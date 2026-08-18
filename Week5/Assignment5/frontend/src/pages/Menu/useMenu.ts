import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosClient from "../../api/axiosClient";
import { FoodItem, Restaurant } from "../../types";

export function useMenu() {
  const { restaurantId } = useParams();
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [items, setItems] = useState<FoodItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!restaurantId) return;
    Promise.all([
      axiosClient.get(`/restaurants/${restaurantId}`),
      axiosClient.get(`/food-items?restaurant_id=${restaurantId}`),
    ])
      .then(([restaurantRes, itemsRes]) => {
        setRestaurant(restaurantRes.data);
        setItems(itemsRes.data);
      })
      .catch(() => setError("Could not load menu"))
      .finally(() => setLoading(false));
  }, [restaurantId]);

  return { restaurant, items, loading, error };
}
