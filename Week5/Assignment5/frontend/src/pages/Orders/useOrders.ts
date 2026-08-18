import { useEffect, useState } from "react";
import axiosClient from "../../api/axiosClient";
import { Order } from "../../types";

export function useOrders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axiosClient
      .get("/orders")
      .then((res) => setOrders(res.data))
      .catch(() => setError("Could not load orders"))
      .finally(() => setLoading(false));
  }, []);

  return { orders, loading, error };
}
