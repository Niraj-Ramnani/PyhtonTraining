import { Link } from "react-router-dom";
import { Restaurant } from "../../types";
import "./RestaurantCard.css";

interface Props {
  restaurant: Restaurant;
}

export default function RestaurantCard({ restaurant }: Props) {
  return (
    <Link to={`/restaurants/${restaurant.restaurant_id}`} className="restaurant-card card">
      <h3>{restaurant.name}</h3>
      <p className="restaurant-address">{restaurant.address}</p>
      <span className="restaurant-rating">⭐ {restaurant.rating.toFixed(1)}</span>
    </Link>
  );
}
