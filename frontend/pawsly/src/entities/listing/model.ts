import type { Listing } from '@/types'

export const DEMO_LISTINGS: Listing[] = [
  { id: '1', owner_id: 'u1', pet: { id: 'p1', owner_id: 'u1', name: 'Бобик', species: 'dog', breed: 'Лабрадор', age: 3, is_active: true }, date_start: '2026-07-14', date_end: '2026-07-18', price_per_day: 500, description: 'Добрый пёс, знает команды, нужны 2 прогулки в день', status: 'open', created_at: '' },
  { id: '2', owner_id: 'u2', pet: { id: 'p2', owner_id: 'u2', name: 'Мурка', species: 'cat', breed: 'Мейн-кун', age: 5, is_active: true }, date_start: '2026-07-20', date_end: '2026-07-25', price_per_day: 300, status: 'open', created_at: '' },
  { id: '3', owner_id: 'u3', pet: { id: 'p3', owner_id: 'u3', name: 'Хомяш', species: 'rodent', age: 1, is_active: true }, date_start: '2026-08-01', date_end: '2026-08-07', price_per_day: 150, status: 'open', created_at: '' },
]

export const LISTINGS_KEY = 'pawsly-listings'
export const SPECIES_LABELS = { dog: 'Собака', cat: 'Кошка', bird: 'Птица', rodent: 'Грызун', reptile: 'Рептилия', other: 'Другое' } as const

export function formatDate(date: string) {
  return new Date(`${date}T00:00:00`).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

export function listingDays(listing: Listing) {
  return Math.max(1, Math.round((new Date(listing.date_end).getTime() - new Date(listing.date_start).getTime()) / 86400000))
}
