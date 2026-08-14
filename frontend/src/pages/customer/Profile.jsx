import { useState } from "react";
import toast from "react-hot-toast";
import { FiEdit2 } from "react-icons/fi";
import { useAuth } from "../../context/AuthContext";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import StatusBadge from "../../components/ui/StatusBadge";
import ProfileAvatarUpload from "../../components/profile/ProfileAvatarUpload";
import ProfileInfoRow from "../../components/profile/ProfileInfoRow";
import ProfileDetailsForm from "../../components/profile/ProfileDetailsForm";
import { MOCK_PROFILE } from "../../constants/mockProfile";
import { formatDate } from "../../utils/format";

export default function CustomerProfile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(MOCK_PROFILE);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  const initials = (profile.fullName || user?.email || "?")[0]?.toUpperCase();

  function handleAvatarChange(dataUrl) {
    // Local-only preview — no upload endpoint exists yet.
    setProfile((prev) => ({ ...prev, avatarUrl: dataUrl }));
    toast.success("Profile picture updated.");
  }

  function handleSave(values) {
    setSaving(true);
    // Simulated save — swap for a real API call once the backend exposes
    // a profile endpoint. Business logic stays out of the UI layer either way.
    setTimeout(() => {
      setProfile((prev) => ({ ...prev, ...values }));
      setSaving(false);
      setEditing(false);
      toast.success("Profile updated.");
    }, 500);
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">My profile</h2>
        <p className="mt-1 text-sm text-ink-faint">Your personal and contact details.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left: identity summary */}
        <Card className="lg:col-span-1 flex flex-col items-center text-center">
          <ProfileAvatarUpload
            avatarUrl={profile.avatarUrl}
            initials={initials}
            onChange={handleAvatarChange}
          />
          <h3 className="mt-4 font-display text-lg text-ink">{profile.fullName}</h3>
          <p className="text-sm text-ink-faint">{user?.email}</p>

          <div className="mt-5 w-full space-y-3 border-t border-line pt-5 text-left">
            <ProfileInfoRow label="Customer ID" value={profile.customerId} />
            <div className="leader-row text-sm">
              <span className="text-ink-faint">Account status</span>
              <span className="leader-fill" />
              <StatusBadge status={profile.accountStatus} />
            </div>
            <ProfileInfoRow label="Joined" value={formatDate(profile.joinedDate)} />
            <ProfileInfoRow label="Current plan" value={profile.currentPlan} />
          </div>
        </Card>

        {/* Right: editable details */}
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-lg text-ink">Contact details</h3>
            {!editing && (
              <Button variant="secondary" icon={<FiEdit2 size={13} />} onClick={() => setEditing(true)}>
                Edit
              </Button>
            )}
          </div>

          <div className="mt-5">
            {editing ? (
              <ProfileDetailsForm
                values={profile}
                onSave={handleSave}
                onCancel={() => setEditing(false)}
                saving={saving}
              />
            ) : (
              <div className="space-y-3.5">
                <ProfileInfoRow label="Full name" value={profile.fullName} />
                <ProfileInfoRow label="Phone number" value={profile.phone} />
                <ProfileInfoRow label="Address" value={profile.address} />
                <ProfileInfoRow label="City" value={profile.city} />
                <ProfileInfoRow label="State" value={profile.state} />
                <ProfileInfoRow label="Country" value={profile.country} />
                <ProfileInfoRow label="Pincode" value={profile.pincode} />
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
