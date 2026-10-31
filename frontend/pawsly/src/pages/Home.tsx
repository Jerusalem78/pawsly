import { useMemo, useState } from 'react'
import { Badge, Button, Modal, ModalFooter, FormGroup, Input, Textarea } from '@/components/ui'
import type { Listing } from '@/types'
import { DEMO_LISTINGS, LISTINGS_KEY } from '@/entities/listing/model'
import { readStorage, writeStorage } from '@/shared/lib/storage'

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
  const [listings] = useState<Listing[]>(() => readStorage(LISTINGS_KEY, DEMO_LISTINGS))
  const [selected, setSelected] = useState<Listing | null>(null)
  const [message, setMessage] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [filters, setFilters] = useState({ species: '', min: '', max: '' })
  const [dateStart, setDateStart] = useState('')
  const [dateEnd, setDateEnd] = useState('')
  const visibleListings = useMemo(() => listings.filter(item => item.status === 'open'
    && (!filters.species || item.pet.species === filters.species)
    && (!filters.min || item.price_per_day >= Number(filters.min))
    && (!filters.max || item.price_per_day <= Number(filters.max))
    && (!dateStart || item.date_start <= dateStart)
    && (!dateEnd || item.date_end >= dateEnd)), [listings, filters, dateStart, dateEnd])

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex items-start justify-between mb-7">
        <div>
          <h1 className="text-[26px] font-semibold tracking-tight">Найти ситтера</h1>
          <p className="text-[14px] text-[#a1a1a6] mt-1">Надёжный уход за вашим питомцем</p>
        </div>
      </div>

      <div className="flex gap-2.5 mb-6 flex-wrap">
        <input aria-label="Дата с" value={dateStart} onChange={e => setDateStart(e.target.value)} className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff]" type="date" />
        <input aria-label="Дата по" value={dateEnd} min={dateStart || undefined} onChange={e => setDateEnd(e.target.value)} className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff]" type="date" />
        <select value={filters.species} onChange={e => setFilters(f => ({ ...f, species: e.target.value }))} className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] font-[inherit] outline-none focus:border-[#5e9bff] cursor-pointer">
          <option value="">Все животные</option>
          <option value="dog">🐶 Собаки</option><option value="cat">🐱 Кошки</option><option value="bird">🐦 Птицы</option><option value="rodent">🐹 Грызуны</option><option value="reptile">🦎 Рептилии</option>
        </select>
        <input aria-label="Цена от" placeholder="Цена от" value={filters.min} onChange={e => setFilters(f => ({ ...f, min: e.target.value }))} className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] w-24 font-[inherit] outline-none focus:border-[#5e9bff] placeholder:text-[#636366]" type="number" min="0" />
        <input aria-label="Цена до" placeholder="Цена до" value={filters.max} onChange={e => setFilters(f => ({ ...f, max: e.target.value }))} className="px-3.5 py-2 bg-[#141414] border border-white/[0.08] rounded-lg text-[#f5f5f7] text-[13px] w-24 font-[inherit] outline-none focus:border-[#5e9bff] placeholder:text-[#636366]" type="number" min="0" />
      </div>

      <div className="grid grid-cols-3 gap-4 max-[720px]:grid-cols-2 max-[480px]:grid-cols-1">
        {visibleListings.map(l => {
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
        {visibleListings.length === 0 && <p className="col-span-full text-center py-12 text-[#a1a1a6]">По заданным фильтрам объявлений нет.</p>}
      </div>

      <Modal open={!!selected} onClose={() => { setSelected(null); setSubmitted(false); setMessage('') }} title={selected ? `${SPECIES_EMOJI[selected.pet.species]} ${selected.pet.name}` : ''}>
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
            {submitted && <p role="status" className="text-sm text-[#30d158]">Отклик сохранён в демо-режиме.</p>}
            <ModalFooter>
              <Button onClick={() => { setSelected(null); setSubmitted(false); setMessage('') }}>Закрыть</Button>
              <Button variant="primary" onClick={() => { const apps = readStorage<{ listingId: string; message: string }[]>('pawsly-applications', []); writeStorage('pawsly-applications', [...apps, { listingId: selected.id, message }]); setSubmitted(true) }}>Откликнуться</Button>
            </ModalFooter>
          </>
        )}
      </Modal>
    </div>
  )
}
