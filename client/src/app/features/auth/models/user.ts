export interface Location {
  latitude: number;
  longitude: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  location?: Location;
}


