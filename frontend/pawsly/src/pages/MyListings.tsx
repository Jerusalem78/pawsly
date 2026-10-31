import { useState } from 'react'
import type { FormEvent } from 'react'
import { Badge, Button, Modal, ModalFooter, FormGroup, Input, Select, Textarea } from '@/components/ui'
import type { Listing, Pet } from '@/types'
import { DEMO_LISTINGS, formatDate, listingDays, LISTINGS_KEY } from '@/entities/listing/model'
import { readStorage, writeStorage } from '@/shared/lib/storage'
import { FieldError } from '@/shared/ui/FieldError'

export default function MyListings() {
  const [listings, setListings] = useState<Listing[]>(() => readStorage(LISTINGS_KEY, DEMO_LISTINGS))
  const [pets] = useState<Pet[]>(() => readStorage('pawsly-pets', []))
  const [open, setOpen] = useState(false)
  const [petId, setPetId] = useState(pets[0]?.id ?? '')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [price, setPrice] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  function publish(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const pet = pets.find(item => item.id === petId)
    if (!pet) { setError('Сначала добавьте питомца в разделе «Питомцы»'); return }
    if (!start || !end || new Date(start) >= new Date(end)) { setError('Укажите корректный период: дата окончания должна быть позже начала'); return }
    if (!Number.isInteger(Number(price)) || Number(price) < 1) { setError('Цена должна быть целым числом больше нуля'); return }
    const value: Listing = { id: Date.now().toString(), owner_id: 'me', pet, date_start: start, date_end: end, price_per_day: Number(price), description: description.trim(), status: 'open', created_at: new Date().toISOString() }
    const next = [value, ...listings]
    setListings(next); writeStorage(LISTINGS_KEY, next); setOpen(false); setError('')
    setStart(''); setEnd(''); setPrice(''); setDescription('')
  }

  function closeListing(id: string) {
    const next = listings.map(item => item.id === id ? { ...item, status: 'closed' as const } : item)
    setListings(next); writeStorage(LISTINGS_KEY, next)
  }

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex items-start justify-between mb-7">
        <div><h1 className="text-[26px] font-semibold tracking-tight">Мои объявления</h1><p className="text-[14px] text-[#a1a1a6] mt-1">Объявления о поиске ситтера сохраняются в этом браузере</p></div>
        <Button variant="primary" onClick={() => { setPetId(pets[0]?.id ?? ''); setOpen(true) }}>+ Создать</Button>
      </div>
      {listings.length === 0 ? <div className="text-center py-16 text-[#a1a1a6]"><div className="text-5xl mb-4">📋</div><p className="text-[#f5f5f7] mb-4">Объявлений пока нет</p><Button variant="primary" onClick={() => setOpen(true)}>Создать объявление</Button></div> :
        <div className="flex flex-col gap-3">{listings.map(listing => {
          const days = listingDays(listing)
          return <article key={listing.id} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5 transition-all duration-200 hover:border-white/[0.16]">
            <div className="flex justify-between items-start mb-3"><div><h2 className="text-[15px] font-medium">Уход за {listing.pet.name}</h2><p className="text-[13px] text-[#a1a1a6] mt-1">{formatDate(listing.date_start)} — {formatDate(listing.date_end)} · {listing.price_per_day} ₽/день · Итого {listing.price_per_day * days} ₽</p></div><Badge variant={listing.status === 'open' ? 'green' : 'gray'}>{listing.status === 'open' ? 'Открыто' : 'Закрыто'}</Badge></div>
            {listing.description && <p className="text-sm text-[#a1a1a6]">{listing.description}</p>}
            {listing.status === 'open' && <div className="mt-4"><Button size="sm" variant="danger" onClick={() => closeListing(listing.id)}>Закрыть объявление</Button></div>}
          </article>
        })}</div>}
      <Modal open={open} onClose={() => { setOpen(false); setError('') }} title="Создать объявление">
        <form onSubmit={publish} noValidate>
          <FormGroup label="Питомец"><Select value={petId} onChange={event => setPetId(event.target.value)}><option value="">Выберите питомца</option>{pets.map(pet => <option key={pet.id} value={pet.id}>{pet.name}</option>)}</Select></FormGroup>
          <FormGroup label="Дата начала"><Input type="date" value={start} onChange={event => setStart(event.target.value)} /></FormGroup>
          <FormGroup label="Дата окончания"><Input type="date" value={end} onChange={event => setEnd(event.target.value)} /></FormGroup>
          <FormGroup label="Цена за день (₽)"><Input type="number" min="1" step="1" placeholder="500" value={price} onChange={event => setPrice(event.target.value)} /></FormGroup>
          <FormGroup label="Описание"><Textarea rows={3} placeholder="Пожелания к ситтеру..." value={description} onChange={event => setDescription(event.target.value)} /></FormGroup>
          {error && <FieldError>{error}</FieldError>}
          <ModalFooter><Button type="button" onClick={() => setOpen(false)}>Отмена</Button><Button type="submit" variant="primary">Опубликовать</Button></ModalFooter>
        </form>
      </Modal>
    </div>
  )
}
