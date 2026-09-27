import { Badge, Button } from '@/components/ui'

const ACTIVE = [
  { id: '1', pet: 'Бобик', sitter: 'Иван П.', dates: '14–18 июля', amount: 2500, status: 'escrowed' },
]

const FINISHED = [
  { id: '2', pet: 'Мурка', sitter: 'Мария С.', dates: '1–5 июня', amount: 1500, status: 'completed' },
  { id: '3', pet: 'Бобик', sitter: 'Алексей К.', dates: '10–14 мая', amount: 2000, status: 'cancelled' },
]

const STATUS: Record<string, { label: string; variant: 'blue' | 'green' | 'gray' | 'yellow' }> = {
  escrowed: { label: 'В процессе', variant: 'blue' },
  sitter_done: { label: 'Ожидает подтверждения', variant: 'yellow' },
  completed: { label: 'Завершено', variant: 'green' },
  cancelled: { label: 'Отменено', variant: 'gray' },
}

export default function MyBookings() {
  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="mb-7">
        <h1 className="text-[26px] font-semibold tracking-tight">Бронирования</h1>
        <p className="text-[14px] text-[#a1a1a6] mt-1">Активные и прошлые</p>
      </div>

      <div className="text-[13px] font-medium text-[#636366] uppercase tracking-wider mb-3">Активные</div>
      <div className="flex flex-col gap-3 mb-8">
        {ACTIVE.map(b => {
          const s = STATUS[b.status]
          return (
            <div key={b.id} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <div className="text-[15px] font-medium">{b.pet} · Ситтер: {b.sitter}</div>
                  <div className="text-[13px] text-[#a1a1a6] mt-0.5">{b.dates} · {b.amount} ₽ в эскроу</div>
                </div>
                <Badge variant={s.variant}>{s.label}</Badge>
              </div>
              <div className="flex gap-2">
                <Button variant="primary" size="sm">Подтвердить завершение</Button>
                <Button variant="danger" size="sm">Открыть спор</Button>
              </div>
            </div>
          )
        })}
      </div>

      <div className="text-[13px] font-medium text-[#636366] uppercase tracking-wider mb-3">Завершённые</div>
      <div className="flex flex-col gap-3">
        {FINISHED.map(b => {
          const s = STATUS[b.status]
          return (
            <div key={b.id} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-[15px] font-medium">{b.pet} · Ситтер: {b.sitter}</div>
                  <div className="text-[13px] text-[#a1a1a6] mt-0.5">{b.dates} · {b.amount} ₽</div>
                </div>
                <Badge variant={s.variant}>{s.label}</Badge>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}