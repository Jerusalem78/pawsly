import { useState } from 'react'
import { Badge, Button, Modal, ModalFooter, FormGroup, Input, Select, Textarea } from '@/components/ui'

const DEMO = [
  { id: '1', pet: 'Бобик', dates: '14–18 июля', price: 500, total: 2500, status: 'open', apps: 3 },
  { id: '2', pet: 'Мурка', dates: '1–5 июня', price: 300, total: 1500, status: 'closed', apps: 0 },
]

const STATUS: Record<string, { label: string; variant: 'green' | 'gray' }> = {
  open: { label: 'Открыто', variant: 'green' },
  closed: { label: 'Закрыто', variant: 'gray' },
}

export default function MyListings() {
  const [open, setOpen] = useState(false)

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex items-start justify-between mb-7">
        <div>
          <h1 className="text-[26px] font-semibold tracking-tight">Мои объявления</h1>
          <p className="text-[14px] text-[#a1a1a6] mt-1">Объявления о поиске ситтера</p>
        </div>
        <Button variant="primary" onClick={() => setOpen(true)}>+ Создать</Button>
      </div>

      <div className="flex flex-col gap-3">
        {DEMO.map(l => {
          const s = STATUS[l.status]
          return (
            <div key={l.id} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <div className="text-[15px] font-medium">Уход за {l.pet}</div>
                  <div className="text-[13px] text-[#a1a1a6] mt-0.5">{l.dates} · {l.price} ₽/день · Итого {l.total} ₽</div>
                </div>
                <Badge variant={s.variant}>{s.label}</Badge>
              </div>
              <div className="h-px bg-white/[0.08] my-3" />
              <div className="text-[13px] text-[#a1a1a6] mb-3">{l.apps} заявок</div>
              {l.status === 'open' && (
                <div className="flex gap-2">
                  <Button size="sm">Смотреть заявки</Button>
                  <Button size="sm">Изменить</Button>
                  <Button size="sm" variant="danger">Закрыть</Button>
                </div>
              )}
            </div>
          )
        })}
      </div>

      <Modal open={open} onClose={() => setOpen(false)} title="Создать объявление">
        <FormGroup label="Питомец">
          <Select>
            <option>Бобик</option>
            <option>Мурка</option>
          </Select>
        </FormGroup>
        <FormGroup label="Дата начала"><Input type="date" /></FormGroup>
        <FormGroup label="Дата конца"><Input type="date" /></FormGroup>
        <FormGroup label="Цена за день (₽)"><Input type="number" placeholder="500" /></FormGroup>
        <FormGroup label="Описание"><Textarea rows={3} placeholder="Пожелания к ситтеру..." /></FormGroup>
        <ModalFooter>
          <Button onClick={() => setOpen(false)}>Отмена</Button>
          <Button variant="primary" onClick={() => setOpen(false)}>Опубликовать</Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}