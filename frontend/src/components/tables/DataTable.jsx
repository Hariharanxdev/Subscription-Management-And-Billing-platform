import { useMemo, useState } from "react";
import { FiChevronLeft, FiChevronRight, FiChevronUp, FiChevronDown, FiSearch } from "react-icons/fi";
import { SkeletonRow } from "../ui/Loader";

const PAGE_SIZE = 8;

/**
 * columns: [{ key, header, render?(row), sortable?, sortValue?(row) }]
 */
export default function DataTable({
  columns,
  data = [],
  loading = false,
  searchable = true,
  searchPlaceholder = "Search…",
  searchKeys = [],
  emptyState,
  rowKey = (row) => row.id,
}) {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState({ key: null, dir: "asc" });
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    if (!query || searchKeys.length === 0) return data;
    const q = query.toLowerCase();
    return data.filter((row) =>
      searchKeys.some((key) => String(row[key] ?? "").toLowerCase().includes(q))
    );
  }, [data, query, searchKeys]);

  const sorted = useMemo(() => {
    if (!sort.key) return filtered;
    const col = columns.find((c) => c.key === sort.key);
    const getValue = col?.sortValue || ((row) => row[sort.key]);
    return [...filtered].sort((a, b) => {
      const av = getValue(a);
      const bv = getValue(b);
      if (av === bv) return 0;
      const result = av > bv ? 1 : -1;
      return sort.dir === "asc" ? result : -result;
    });
  }, [filtered, sort, columns]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
  const pageSafe = Math.min(page, totalPages);
  const pageData = sorted.slice((pageSafe - 1) * PAGE_SIZE, pageSafe * PAGE_SIZE);

  function toggleSort(key) {
    setSort((prev) =>
      prev.key === key ? { key, dir: prev.dir === "asc" ? "desc" : "asc" } : { key, dir: "asc" }
    );
  }

  return (
    <div>
      {searchable && (
        <div className="mb-4 flex items-center gap-3">
          <div className="relative w-full max-w-xs">
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-faint" size={15} />
            <input
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setPage(1);
              }}
              placeholder={searchPlaceholder}
              className="input pl-9"
            />
          </div>
          <span className="text-xs text-ink-faint tabular ml-auto">
            {sorted.length} {sorted.length === 1 ? "record" : "records"}
          </span>
        </div>
      )}

      <div className="overflow-x-auto rounded-xl border border-line">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-line bg-paper-dim/50 text-left">
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => col.sortable && toggleSort(col.key)}
                  className={`px-4 py-3 text-xs font-semibold uppercase tracking-wider text-ink-faint whitespace-nowrap ${
                    col.sortable ? "cursor-pointer select-none hover:text-ink-soft" : ""
                  }`}
                >
                  <span className="inline-flex items-center gap-1">
                    {col.header}
                    {col.sortable && sort.key === col.key && (
                      sort.dir === "asc" ? <FiChevronUp size={12} /> : <FiChevronDown size={12} />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {loading &&
              Array.from({ length: 4 }).map((_, i) => (
                <tr key={i}>
                  <td colSpan={columns.length} className="px-4">
                    <SkeletonRow />
                  </td>
                </tr>
              ))}

            {!loading && pageData.length === 0 && (
              <tr>
                <td colSpan={columns.length}>
                  {emptyState || (
                    <p className="py-12 text-center text-sm text-ink-faint">No records found.</p>
                  )}
                </td>
              </tr>
            )}

            {!loading &&
              pageData.map((row) => (
                <tr key={rowKey(row)} className="hover:bg-ink/[0.015] transition-colors">
                  {columns.map((col) => (
                    <td key={col.key} className="px-4 py-3.5 align-middle text-ink-soft whitespace-nowrap">
                      {col.render ? col.render(row) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {!loading && totalPages > 1 && (
        <div className="mt-4 flex items-center justify-between">
          <p className="text-xs text-ink-faint tabular">
            Page {pageSafe} of {totalPages}
          </p>
          <div className="flex gap-2">
            <button
              className="btn-secondary !px-3 !py-1.5"
              disabled={pageSafe === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              <FiChevronLeft size={14} />
            </button>
            <button
              className="btn-secondary !px-3 !py-1.5"
              disabled={pageSafe === totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              <FiChevronRight size={14} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
