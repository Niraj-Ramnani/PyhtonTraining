import RestaurantCard from "../../components/RestaurantCard/RestaurantCard";
import { useRestaurants } from "./useRestaurants";
import "./Restaurants.css";

export default function Restaurants() {
  const { restaurants, loading, error } = useRestaurants();

  if (loading) return <div className="page">Loading restaurants...</div>;
  if (error) return <div className="page error-text">{error}</div>;

  return (
    <div className="page">
      <h2>Restaurants</h2>
      <div className="restaurant-list">
        {restaurants.map((r) => (
          <RestaurantCard key={r.restaurant_id} restaurant={r} />
        ))}
      </div>
    </div>
  );
}
