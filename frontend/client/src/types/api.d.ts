export interface Credentials {
  email: string;
  password: string;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: string;
  timestamp: number;
}

export interface UserForm {
  credentials: Credentials;
  name: string;
}

export interface ValidationError {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface Operation {
  id: number;
  title: string;
  status: string;
  // Define other operation properties based on API
}

export interface Client {
  id: number;
  name: string;
  email: string;
  // Define other client properties based on API
} 