import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FiDownload } from "react-icons/fi";
import { invoiceService } from "../../services/invoiceService";
import DataTable from "../../components/tables/DataTable";
import StatusBadge from "../../components/ui/StatusBadge";
import Button from "../../components/ui/Button";
import ErrorState from "../../components/ui/ErrorState";
import { formatCurrency, formatDate, extractErrorMessage } from "../../utils/format";

export default function CustomerInvoices() {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [downloadingId, setDownloadingId] = useState(null);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await invoiceService.getMine();
      setInvoices(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleDownload(invoice) {
    setDownloadingId(invoice.id);
    try {
      await invoiceService.downloadPdf(invoice.id, `${invoice.invoice_number}.pdf`);
    } catch (err) {
      toast.error(extractErrorMessage(err) || "Couldn't download the invoice.");
    } finally {
      setDownloadingId(null);
    }
  }

  const columns = [
    { key: "invoice_number", header: "Invoice", render: (r) => <span className="tabular font-medium text-ink">{r.invoice_number}</span> },
    { key: "issued_at", header: "Issued", sortable: true, render: (r) => <span className="tabular">{formatDate(r.issued_at)}</span> },
    { key: "amount", header: "Amount", sortable: true, render: (r) => <span className="tabular font-medium">{formatCurrency(r.amount)}</span> },
    { key: "status", header: "Status", render: (r) => <StatusBadge status={r.status} /> },
    {
      key: "actions",
      header: "",
      render: (r) => (
        <Button
          variant="secondary"
          className="!px-3 !py-1.5 !text-xs"
          loading={downloadingId === r.id}
          icon={<FiDownload size={13} />}
          onClick={() => handleDownload(r)}
        >
          PDF
        </Button>
      ),
    },
  ];

  if (error) return <ErrorState message="Couldn't load your invoices." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">Invoices</h2>
        <p className="mt-1 text-sm text-ink-faint">Generated automatically the moment a payment succeeds.</p>
      </div>

      <DataTable
        columns={columns}
        data={invoices}
        loading={loading}
        searchKeys={["invoice_number", "status"]}
        searchPlaceholder="Search invoices…"
        emptyState={<p className="py-12 text-center text-sm text-ink-faint">No invoices yet.</p>}
      />
    </div>
  );
}
