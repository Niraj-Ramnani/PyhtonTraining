import { useEffect, useState } from "react";
import axiosClient from "../../api/axiosClient";
import { Restaurant } from "../../types";

export function useRestaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axiosClient
      .get("/restaurants")
      .then((res) => setRestaurants(res.data))
      .catch(() => setError("Could not load restaurants"))
      .finally(() => setLoading(false));
  }, []);

  return { restaurants, loading, error };
}
