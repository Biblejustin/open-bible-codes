#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

using namespace std;

struct TermRow {
    string term_id;
    vector<uint32_t> query;
};

struct HitRow {
    string term_id;
    int normalized_length;
    string mode;
    int min_skip;
    int effective_max_skip;
    int skip;
    int start_offset;
    int end_offset;
};

struct PositionIndex {
    unordered_map<uint32_t, vector<int>> by_char;
};

static vector<uint32_t> utf8_codepoints(const string &s) {
    vector<uint32_t> out;
    for (size_t i = 0; i < s.size();) {
        unsigned char c = static_cast<unsigned char>(s[i]);
        if (c < 0x80) {
            out.push_back(c);
            i += 1;
        } else if ((c >> 5) == 0x6) {
            out.push_back(((c & 0x1F) << 6) | (s[i + 1] & 0x3F));
            i += 2;
        } else if ((c >> 4) == 0xE) {
            out.push_back(
                ((c & 0x0F) << 12) |
                ((s[i + 1] & 0x3F) << 6) |
                (s[i + 2] & 0x3F)
            );
            i += 3;
        } else {
            out.push_back(
                ((c & 0x07) << 18) |
                ((s[i + 1] & 0x3F) << 12) |
                ((s[i + 2] & 0x3F) << 6) |
                (s[i + 3] & 0x3F)
            );
            i += 4;
        }
    }
    return out;
}

static string read_file(const string &path) {
    ifstream handle(path, ios::binary);
    if (!handle) {
        throw runtime_error("cannot open " + path);
    }
    return string((istreambuf_iterator<char>(handle)), {});
}

static vector<string> split_tab(const string &line) {
    vector<string> parts;
    string item;
    stringstream stream(line);
    while (getline(stream, item, '\t')) {
        parts.push_back(item);
    }
    return parts;
}

static vector<TermRow> read_terms(const string &path) {
    ifstream handle(path);
    if (!handle) {
        throw runtime_error("cannot open " + path);
    }
    vector<TermRow> rows;
    string line;
    while (getline(handle, line)) {
        if (line.empty()) {
            continue;
        }
        auto parts = split_tab(line);
        if (parts.size() < 2) {
            throw runtime_error("bad term row: " + line);
        }
        rows.push_back({parts[0], utf8_codepoints(parts[1])});
    }
    return rows;
}

static PositionIndex build_position_index(const vector<uint32_t> &text) {
    PositionIndex index;
    index.by_char.reserve(128);
    for (int i = 0; i < static_cast<int>(text.size()); ++i) {
        index.by_char[text[i]].push_back(i);
    }
    return index;
}

static const vector<int> empty_positions;

static const vector<int> &positions_for(const PositionIndex &index, uint32_t codepoint) {
    auto found = index.by_char.find(codepoint);
    if (found == index.by_char.end()) {
        return empty_positions;
    }
    return found->second;
}

static void collect_forward_pair_index_hits(
    const vector<uint32_t> &text,
    const PositionIndex &index,
    const TermRow &term,
    int min_skip,
    int max_skip,
    int signed_skip_factor,
    const string &mode,
    long long max_hits,
    vector<HitRow> &hits
) {
    const int n = static_cast<int>(text.size());
    const int k = static_cast<int>(term.query.size());
    if (k <= 0 || max_skip < min_skip) {
        return;
    }
    if (k == 1) {
        const auto &positions = positions_for(index, term.query[0]);
        for (int position : positions) {
            hits.push_back({term.term_id, k, mode, min_skip, max_skip, signed_skip_factor, position, position});
            if (max_hits > 0 && static_cast<long long>(hits.size()) >= max_hits) {
                return;
            }
        }
        return;
    }

    long long best_cost = numeric_limits<long long>::max();
    int left_index = 0;
    int right_index = 1;
    for (int i = 0; i < k; ++i) {
        for (int j = i + 1; j < k; ++j) {
            const auto &left_positions = positions_for(index, term.query[i]);
            const auto &right_positions = positions_for(index, term.query[j]);
            long long cost =
                static_cast<long long>(left_positions.size()) *
                static_cast<long long>(right_positions.size()) /
                max(1, j - i);
            if (cost < best_cost) {
                best_cost = cost;
                left_index = i;
                right_index = j;
            }
        }
    }

    const auto &left_positions = positions_for(index, term.query[left_index]);
    const auto &right_positions = positions_for(index, term.query[right_index]);
    if (left_positions.empty() || right_positions.empty()) {
        return;
    }

    const int delta = right_index - left_index;
    vector<vector<int>> buckets(delta);
    for (int position : right_positions) {
        buckets[position % delta].push_back(position);
    }
    for (auto &bucket : buckets) {
        sort(bucket.begin(), bucket.end());
    }

    vector<int> check_order;
    for (int i = 0; i < k; ++i) {
        if (i != left_index && i != right_index) {
            check_order.push_back(i);
        }
    }
    sort(check_order.begin(), check_order.end(), [&](int a, int b) {
        return positions_for(index, term.query[a]).size() < positions_for(index, term.query[b]).size();
    });

    for (int left_position : left_positions) {
        long long low = static_cast<long long>(left_position) + static_cast<long long>(delta) * min_skip;
        long long high = static_cast<long long>(left_position) + static_cast<long long>(delta) * max_skip;
        if (low > n - 1) {
            continue;
        }
        high = min<long long>(high, n - 1);
        auto &bucket = buckets[left_position % delta];
        auto it = lower_bound(bucket.begin(), bucket.end(), static_cast<int>(low));
        auto end = upper_bound(bucket.begin(), bucket.end(), static_cast<int>(high));
        for (; it != end; ++it) {
            int right_position = *it;
            int diff = right_position - left_position;
            if (diff % delta != 0) {
                continue;
            }
            int skip = diff / delta;
            int start = left_position - left_index * skip;
            int finish = start + (k - 1) * skip;
            if (start < 0 || finish >= n) {
                continue;
            }
            bool ok = true;
            for (int query_index : check_order) {
                if (text[start + query_index * skip] != term.query[query_index]) {
                    ok = false;
                    break;
                }
            }
            if (!ok) {
                continue;
            }
            if (signed_skip_factor > 0) {
                hits.push_back({term.term_id, k, mode, min_skip, max_skip, skip, start, finish});
            } else {
                hits.push_back({term.term_id, k, mode, min_skip, max_skip, -skip, finish, start});
            }
            if (max_hits > 0 && static_cast<long long>(hits.size()) >= max_hits) {
                return;
            }
        }
    }
}

static int max_skip_for_mode(int text_length, int query_length, const string &mode) {
    if (query_length <= 0) {
        return 0;
    }
    if (mode == "letters-per-term") {
        return max(1, text_length / query_length);
    }
    if (mode == "full-span") {
        if (query_length <= 1) {
            return max(1, text_length - 1);
        }
        return max(1, (text_length - 1) / (query_length - 1));
    }
    throw runtime_error("unsupported mode: " + mode);
}

static string csv_escape(const string &value) {
    if (value.find_first_of(",\"\n") == string::npos) {
        return value;
    }
    string escaped = "\"";
    for (char c : value) {
        if (c == '"') {
            escaped += "\"\"";
        } else {
            escaped += c;
        }
    }
    escaped += '"';
    return escaped;
}

int main(int argc, char **argv) {
    if (argc < 8) {
        cerr << "usage: dynamic_span_hits TEXT TERMS_TSV MIN_SKIP MODE DIRECTION MAX_HITS_PER_TERM OUT_CSV [MAX_SKIP]\n";
        return 2;
    }
    string text_path = argv[1];
    string terms_path = argv[2];
    int min_skip = stoi(argv[3]);
    string mode = argv[4];
    string direction = argv[5];
    long long max_hits_per_term = stoll(argv[6]);
    string out_path = argv[7];
    int requested_max_skip = 0;
    if (argc >= 9) {
        requested_max_skip = stoi(argv[8]);
    }

    vector<uint32_t> text = utf8_codepoints(read_file(text_path));
    PositionIndex index = build_position_index(text);
    vector<TermRow> terms = read_terms(terms_path);

    ofstream out(out_path);
    if (!out) {
        throw runtime_error("cannot open " + out_path);
    }
    out << "term_id,normalized_length,mode,min_skip,effective_max_skip,skip,start_offset,end_offset\n";

    for (const auto &source_term : terms) {
        int dynamic_max_skip = max_skip_for_mode(static_cast<int>(text.size()), static_cast<int>(source_term.query.size()), mode);
        int max_skip = dynamic_max_skip;
        if (requested_max_skip > 0) {
            max_skip = min(max_skip, requested_max_skip);
        }
        vector<HitRow> hits;
        if (direction == "forward" || direction == "both") {
            collect_forward_pair_index_hits(
                text,
                index,
                source_term,
                min_skip,
                max_skip,
                1,
                mode,
                max_hits_per_term,
                hits
            );
        }
        if ((max_hits_per_term <= 0 || static_cast<long long>(hits.size()) < max_hits_per_term) &&
            (direction == "backward" || direction == "both")) {
            auto reversed = source_term;
            reverse(reversed.query.begin(), reversed.query.end());
            collect_forward_pair_index_hits(
                text,
                index,
                reversed,
                min_skip,
                max_skip,
                -1,
                mode,
                max_hits_per_term,
                hits
            );
        }
        sort(hits.begin(), hits.end(), [](const HitRow &a, const HitRow &b) {
            return tie(a.term_id, a.skip, a.start_offset, a.end_offset) <
                   tie(b.term_id, b.skip, b.start_offset, b.end_offset);
        });
        for (const auto &hit : hits) {
            out << csv_escape(hit.term_id) << ","
                << hit.normalized_length << ","
                << hit.mode << ","
                << hit.min_skip << ","
                << hit.effective_max_skip << ","
                << hit.skip << ","
                << hit.start_offset << ","
                << hit.end_offset << "\n";
        }
    }
    return 0;
}
