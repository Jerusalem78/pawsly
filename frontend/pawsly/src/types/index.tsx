export type Species = 'dog' | 'cat' | 'bird' | 'rodent' | 'reptile' | 'other'
export type Role = 'owner' | 'sitter' | 'admin'
export type ListingStatus = 'open' | 'matched' | 'closed'
export type BookingStatus = 'pending_payment' | 'escrowed' | 'sitter_done' | 'completed' | 'disputed' | 'resolved_owner' | 'resolved_sitter' | 'resolved_split' | 'cancelled'
export type ApplicationStatus = 'pending' | 'accepted' | 'rejected'
export type TransactionType = 'deposit' | 'escrow_hold' | 'escrow_release' | 'payout' | 'refund' | 'split_payout' | 'split_refund'

export interface User {
  id: string
  username: string
  email: string
  role: Role
  is_active: boolean
  created_at: string
}

export interface Pet {
  id: string
  owner_id: string
  name: string
  species: Species
  breed?: string
  age?: number
  special_notes?: string
  is_active: boolean
}

export interface Listing {
  id: string
  owner_id: string
  pet: Pet
  date_start: string
  date_end: string
  price_per_day: number
  description?: string
  status: ListingStatus
  created_at: string
}

export interface Application {
  id: string
  listing: Listing
  sitter: User
  message?: string
  status: ApplicationStatus
  created_at: string
}

export interface Booking {
  id: string
  listing: Listing
  owner: User
  sitter: User
  total_amount: number
  status: BookingStatus
  sitter_done_at?: string
  owner_confirmed_at?: string
  created_at: string
}

export interface Wallet {
  id: string
  balance: number
  escrow_balance: number
}

export interface Transaction {
  id: string
  amount: number
  type: TransactionType
  ref_id?: string
  created_at: string
}