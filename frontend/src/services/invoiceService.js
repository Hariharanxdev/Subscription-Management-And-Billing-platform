import { apiClient } from "./apiClient";

export const invoiceService = {
  getMine() {
    return apiClient.get("/invoices/me");
  },
  getAll() {
    return apiClient.get("/invoices/");
  },
  getById(id) {
    return apiClient.get(`/invoices/${id}`);
  },
  // The PDF route needs the Authorization header, so it can't be a plain
  // <a href>. We fetch it as a blob and trigger the download manually.
  async downloadPdf(id, filename) {
    const response = await apiClient.get(`/invoices/${id}/pdf`, {
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename || `invoice-${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};
