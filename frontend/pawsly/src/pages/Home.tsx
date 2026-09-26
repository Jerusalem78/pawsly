import { useState } from 'react'
import { Badge, Button, Modal, ModalFooter, FormGroup, Input, Textarea } from '@/components/ui'
import type { Listing } from '@/types'

const LISTINGS: Listing[] = [
  { id: '1', owner_id: 'u1', pet: { id: 'p1', owner_id: 'u1', name: 'Бобик', species: 'dog', breed: 'Лабрадор', age: 3, is_active: true }, date_start: '2026-07-14', date_end: '2026-07-18', price_per_day: 500, description: 'Добрый пёс, знает команды, нужны 2 прогулки в день', status: 'open', created_at: '' },
  { id: '2', owner_id: 'u2', pet: { id: 'p2', owner_id: 'u2', name: 'Мурка', species: 'cat', breed: 'Мейн-кун', age: 5, is_active: true }, date_start: '2026-07-20', date_end: '2026-07-25', price_per_day: 300, status: 'open', created_at: '' },
  { id: '3', owner_id: 'u3', pet: { id: 'p3', owner_id: 'u3', name: 'Хомяш', species: 'rodent', age: 1, is_active: true }, date_start: '2026-08-01', date_end: '2026-08-07', price_per_day: 150, status: 'open', created_at: '' },
  { id: '4', owner_id: 'u4', pet: { id: 'p4', owner_id: 'u4', name: 'Кеша', species: 'bird', breed: 'Попугай', age: 2, is_active: true }, date_start: '2026-08-05', date_end: '2026-08-12', price_per_day: 200, status: 'matched', created_at: '' },
  { id: '5', owner_id: 'u5', pet: { id: 'p5', owner_id: 'u5', name: 'Рекс', species: 'dog', breed: 'Немецкая овчарка', age: 4, is_active: true }, date_start: '2026-08-10', date_end: '2026-08-15', price_per_day: 700, status: 'open', created_at: '' },
  { id: '6', owner_id: 'u6', pet: { id: 'p6', owner_id: 'u6', name: 'Горыныч', species: 'reptile', breed: 'Игуана', age: 3, is_active: true }, date_start: '2026-08-20', date_end: '2026-08-30', price_per_day: 400, status: 'open', created_at: '' },
]

const SPECIES_EMOJI: Record<string, string> = {
  dog: '🐶', cat: '🐱', bird: '🐦', rodent: '🐹', reptile: '🦎', other: '🐾',
}

const STATUS_BADGE: Record<string, { label: string; variant: 'green' | 'blue' | 'gray' }> = {
  open: { label: 'Открыто', variant: 'green' },
  matched: { label: 'Матч найден', variant: 'blue' },
  closed: { label: 'Закрыто', variant: 'gray' },
}

function daysBetween(a: string, b: string) {
  return Math.round((new Date(b).getTime() - new Date(a).getTime()) / 86400000)
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

export default function Home() {
  const [selected, setSelected] = useState<Listing | null>(null)
  const [message, setMessage] = useState('')

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex items-start justify-between mb-7">
        <div>
          <h1 className="text-[26px] font-semibold tracking-tight">Найти ситтера</h1>
          <p className="text-[14px] text-[#a1a1a6] mt-1">Надёжный уход за вашим питомцем</p>
        </div>
      </div>

      <div className="flex gap-2.5 mb-6 flex-wrap">
        <input className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff]" type="date" />
        <input className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff]" type="date" />
        <select className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff] cursor-pointer">
          <option value="">Все животные</option>
          <option>🐶 Собаки</option>
          <option>🐱 Кошки</option>
          <option>🐦 Птицы</option>
          <option>🐹 Грызуны</option>
          <option>🦎 Рептилии</option>
        </select>
        <input placeholder="Цена от" className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] w-24 font-[inherit] outline-none focus:border-[#5e9bff] placeholder:text-[#636366]" type="number" />
        <input placeholder="Цена до" className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] w-24 font-[inherit] outline-none focus:border-[#5e9bff] placeholder:text-[#636366]" type="number" />
        <Button variant="primary">Найти</Button>
      </div>

      <div className="grid grid-cols-3 gap-4 max-[720px]:grid-cols-2 max-[480px]:grid-cols-1">
        {LISTINGS.map(l => {
          const days = daysBetween(l.date_start, l.date_end)
          const s = STATUS_BADGE[l.status]
          return (
            <div
              key={l.id}
              className="bg-[#141414] border border-white/[0.08] rounded-[18px] overflow-hidden cursor-pointer transition-all duration-150 hover:border-white/[0.16]"
              onClick={() => setSelected(l)}
            >
              <div className="h-[140px] bg-[#1c1c1e] flex items-center justify-center text-5xl">
                {SPECIES_EMOJI[l.pet.species]}
              </div>
              <div className="p-4">
                <div className="text-[15px] font-medium mb-1">{l.pet.name} · {l.pet.breed ?? l.pet.species}</div>
                <div className="text-[13px] text-[#a1a1a6] mb-3">
                  {formatDate(l.date_start)} — {formatDate(l.date_end)}
                </div>
                <div className="flex items-center justify-between">
                  <div className="text-[16px] font-semibold text-[#5e9bff]">
                    {l.price_per_day} ₽ <span className="text-[12px] font-normal text-[#a1a1a6]">/ день</span>
                  </div>
                  <Badge variant={s.variant}>{s.label}</Badge>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <Modal open={!!selected} onClose={() => setSelected(null)} title={selected ? `${SPECIES_EMOJI[selected.pet.species]} ${selected.pet.name}` : ''}>
        {selected && (
          <>
            <p className="text-[13px] text-[#a1a1a6] mb-4">
              {formatDate(selected.date_start)} — {formatDate(selected.date_end)} · {daysBetween(selected.date_start, selected.date_end)} дней
            </p>
            {selected.description && (
              <p className="text-[14px] text-[#a1a1a6] mb-4">{selected.description}</p>
            )}
            <div className="h-px bg-white/[0.08] my-4" />
            <div className="flex justify-between mb-4">
              <span className="text-[13px] text-[#a1a1a6]">Цена за день</span>
              <span className="font-semibold">{selected.price_per_day} ₽</span>
            </div>
            <div className="flex justify-between mb-4">
              <span className="text-[13px] text-[#a1a1a6]">Итого</span>
              <span className="font-semibold text-[#5e9bff]">{selected.price_per_day * daysBetween(selected.date_start, selected.date_end)} ₽</span>
            </div>
            <FormGroup label="Сообщение владельцу">
              <Textarea rows={3} placeholder="Расскажите о себе..." value={message} onChange={e => setMessage(e.target.value)} />
            </FormGroup>
            <ModalFooter>
              <Button onClick={() => setSelected(null)}>Закрыть</Button>
              <Button variant="primary" onClick={() => setSelected(null)}>Откликнуться</Button>
            </ModalFooter>
          </>
        )}
      </Modal>
    </div>
  )
}