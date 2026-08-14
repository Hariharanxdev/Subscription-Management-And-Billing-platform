// Placeholder data only. No backend endpoint exists yet for customer profile
// fields (name, phone, address, avatar, etc.) — the real billing backend only
// stores { username, email, role, is_active }. This mock lets the Profile UI
// be built now; swap MOCK_PROFILE for a real fetch once that endpoint exists.
export const MOCK_PROFILE = {
  customerId: "CUST-10234",
  fullName: "Hariharan S",
  phone: "9876543210",
  address: "221B, Anna Nagar 4th Street",
  city: "Chennai",
  state: "Tamil Nadu",
  country: "India",
  pincode: "600040",
  accountStatus: "active",
  joinedDate: "2025-06-12",
  currentPlan: "Pro — Monthly",
  avatarUrl: null,
};

export const COUNTRY_OPTIONS = [
  { value: "India", label: "India" },
  { value: "United States", label: "United States" },
  { value: "United Kingdom", label: "United Kingdom" },
  { value: "United Arab Emirates", label: "United Arab Emirates" },
  { value: "Singapore", label: "Singapore" },
  { value: "Australia", label: "Australia" },
];
