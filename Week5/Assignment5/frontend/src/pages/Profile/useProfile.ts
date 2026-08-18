import { useEffect, useState } from "react";
import axiosClient from "../../api/axiosClient";
import { Profile } from "../../types";

export function useProfile() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    axiosClient
      .get("/profile")
      .then((res) => {
        setProfile(res.data);
        setName(res.data.name);
        setPhone(res.data.phone || "");
      })
      .catch(() => setError("Could not load profile"))
      .finally(() => setLoading(false));
  }, []);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    setError("");
    try {
      const res = await axiosClient.put("/profile", { name, phone });
      setProfile(res.data);
      setSaved(true);
    } catch (err: any) {
      setError(err.response?.data?.error || "Could not update profile");
    } finally {
      setSaving(false);
    }
  }

  return { profile, name, setName, phone, setPhone, loading, saving, error, saved, handleSave };
}
