import { useProfile } from "./useProfile";
import "./Profile.css";

export default function Profile() {
  const { profile, name, setName, phone, setPhone, loading, saving, error, saved, handleSave } = useProfile();

  if (loading) return <div className="page">Loading profile...</div>;

  return (
    <div className="page profile-page">
      <form className="card profile-form" onSubmit={handleSave}>
        <h2>My Profile</h2>
        <label>Email</label>
        <input value={profile?.email} disabled />
        <label>Role</label>
        <input value={profile?.role_name} disabled />
        <label>Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} required />
        <label>Phone</label>
        <input value={phone} onChange={(e) => setPhone(e.target.value)} />
        {error && <p className="error-text">{error}</p>}
        {saved && <p className="success-text">Profile updated!</p>}
        <button className="btn" type="submit" disabled={saving}>
          {saving ? "Saving..." : "Save Changes"}
        </button>
      </form>
    </div>
  );
}
