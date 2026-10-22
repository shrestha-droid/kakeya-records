# Prior-art check via Valency Bond

Run on 22 Oct 2026 with the Valency Bond MCP server (`valency`, server version 0.4.1). The corpus covered arXiv (4.95M papers), PubMed (41.2M), bioRxiv, medRxiv, PsyArXiv, ChemRxiv, SocArXiv, EarthArXiv and Valency Hub, with entries up to 21–22 Oct 2026 (`list_sources`).

**Scope:** Bond returns metadata and abstracts, not full texts. So this check can tell us whether any indexed paper's **abstract** reports a smaller union area. It cannot read numbers that appear only in a paper's tables.

## Queries run

| # | Tool | Query / argument |
|---|---|---|
| 1 | `list_sources` | (none) |
| 2 | `semantic_search_papers` | "Kakeya needle problem thin triangles construction minimal union area, Keich construction" |
| 3 | `search_by_author` | "Keich" |
| 4 | `search_by_author` (fuzzy, to 2002) | "Uri Keich" |
| 5 | `search_by_title` | "Kakeya maximal functions Minkowski dimension" |
| 6 | `search_by_abstract` | "Keich" (category math) |
| 7 | `search_by_abstract` (phrase) | "Perron tree" |
| 8 | `search_by_abstract` | "Kakeya triangles union area" |
| 9 | `semantic_search_papers` | "finite union of thin triangles Kakeya construction minimizing area, Perron tree, Besicovitch set with N triangles, numerical optimization of union area" |
| 10 | `search_by_title` | "AlphaEvolve coding agent scientific algorithmic discovery" |
| 11 | `search_by_title` | "Mathematical exploration and discovery at scale" |
| 12 | `search_by_abstract` | "Kakeya AlphaEvolve" |
| 13 | `semantic_search_papers` (2025 onwards) | "language model or evolutionary search finds improved construction for Kakeya problem with finitely many directions, smaller union area of triangles" |
| 14 | `get_paper_by_id` | 2603.15617 (HorizonMath) |
| 15 | `search_by_abstract` | "HorizonMath" |
| 16 | `get_citing_papers` | 2603.15617 (0 citing papers in the graph) |
| 17 | `get_paper_by_id` | 2304.03633, 2608.23691, 2610.05404, 2610.08927 |
| 18 | `find_similar_papers` | 2608.23691 |
| 19 | `get_citing_papers` | 2608.23691 (0 citing papers in the graph) |

## Relevant papers Bond returned

| Paper | Authors | Year | ID | Relevance |
|---|---|---|---|---|
| Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment | S. Chung, W. Du, W. J. Wesley | 2026 | [arXiv:2608.23691](https://arxiv.org/abs/2608.23691) | **The Dualverse Station paper** (its comments link github.com/dualverse-ai/station). The abstract reports "improved bounds for the discretized Kakeya needle" problem among 12 AlphaEvolve problems. No numbers appear in the abstract. This is the source of the previous-best values. |
| The Station: An Open-World Environment for AI-Driven Discovery | S. Chung, W. Du | 2025 | [arXiv:2511.06309](https://arxiv.org/abs/2511.06309) | The earlier Station environment paper, found as the closest neighbour of 2608.23691. |
| Mathematical exploration and discovery at scale | B. Georgiev, J. Gómez-Serrano, T. Tao, A. Z. Wagner | 2025 | [arXiv:2511.02864](https://arxiv.org/abs/2511.02864); also PNAS 2026, [doi:10.1073/pnas.2536158123](https://doi.org/10.1073/pnas.2536158123) | AlphaEvolve on 67 problems, the source of the AlphaEvolve Kakeya values. No numbers in the abstract. |
| AlphaEvolve: A coding agent for scientific and algorithmic discovery | A. Novikov et al. (18 authors) | 2025 | [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) | The AlphaEvolve system paper. |
| Measuring Progress in Reasoning Toward Mathematical Discovery with Automatic Verification | E. Y. Wang et al. (12 authors) | 2026 | [arXiv:2603.15617](https://arxiv.org/abs/2603.15617) (comment: ICML AI4Math Best Paper Award) | The HorizonMath benchmark (113 problems), which hosts `keich_thin_triangles_128`. Bond's citation graph has 0 citing papers for it. |
| On the generalized Hausdorff dimension of Besicovitch sets | X. Chen, L. Yan, Y. Zhong | 2023 | [arXiv:2304.03633](https://arxiv.org/abs/2304.03633) | The only indexed abstract that names Keich (1999). It is about gauge functions for Besicovitch sets, with no finite-N areas. |
| A construction of Kakeya Sets in Arbitrary Dimension | R. J. Fernández-Delgado, M. de la Salle | 2026 | [arXiv:2607.14824](https://arxiv.org/abs/2607.14824) | Generalises the Perron tree construction to dimension d with δ-neighbourhood volume ≲ \|log δ\|^−(d−1). Asymptotic only. |
| Application of Perron Trees to Geometric Maximal Operators | A. Gauvan | 2022 | [arXiv:2204.02640](https://arxiv.org/abs/2204.02640) | Uses Perron trees for maximal operators. No finite-N areas. |

**Not found:** Keich's 1999 paper on Kakeya maximal functions and Minkowski dimension in R^2 is not indexed in Bond: both author searches return only an unrelated U. Keich (bioinformatics), and a title search gave no match. Bond surfaced it only through the Chen–Yan–Zhong abstract above.

Bond also returned results that are off-topic for finite-N areas: continuum Kakeya theory (Wang–Zahl, Guth, Zahl's survey, star-shaped lower bounds) and other AI-for-math papers on different problems.

## Conclusion

None of the abstracts Bond returned reports a thin-triangle union area below **0.106909** for N = 128, below **0.138432** for N = 32, or below **0.120839** for N = 64. In fact, no returned abstract states any finite-N union area. The prior values used in the README (Keich 1999, AlphaEvolve 2025, GPT-5.4 Pro via HorizonMath 2026, Dualverse Station 2026) sit in full texts or repositories that Bond does not index. They were taken from those primary sources, not from Bond.

Bond did surface one useful fact: the Dualverse Station results come with an arXiv preprint, [arXiv:2608.23691](https://arxiv.org/abs/2608.23691) (24 Aug 2026). Bond's citation graph shows no later work citing it or HorizonMath that could hold a newer record.
