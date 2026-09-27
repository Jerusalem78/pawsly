import { Badge } from '@/components/ui'

const DEMO = [
  { id: '1', pet: '🐶 Лабрадор', dates: '10–15 авг', price: 700, status: 'pending' },
  { id: '2', pet: '🐱 Мейн-кун', dates: '20–25 авг', price: 300, status: 'accepted' },
  { id: '3', pet: '🦎 Игуана', dates: '1–10 сент', price: 400, status: 'rejected' },
]

const STATUS: Record<string, { label: string; variant: 'yellow' | 'green' | 'red' }> = {
  pending: { label: 'Ожидает', variant: 'yellow' },
  accepted: { label: 'Принята', variant: 'green' },
  rejected: { label: 'Отклонена', variant: 'red' },
}

export default function MyApplications() {
  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="mb-7">
        <h1 className="text-[26px] font-semibold tracking-tight">Мои заявки</h1>
        <p className="text-[14px] text-[#a1a1a6] mt-1">Заявки на роль ситтера</p>
      </div>

      <div className="bg-[#141414] border border-white/[0.08] rounded-[18px] overflow-hidden">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              {['Питомец', 'Даты', 'Цена/день', 'Статус', ''].map(h => (
                <th key={h} className="text-left text-[12px] font-medium text-[#636366] px-4 py-2.5 border-b border-white/[0.08] uppercase tracking-wide">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {DEMO.map(a => {
              const s = STATUS[a.status]
              return (
                <tr key={a.id} className="hover:[&>td]:bg-[#1c1c1e]">
                  <td className="px-4 py-3.5 text-[14px] border-b border-white/[0.08]">{a.pet}</td>
                  <td className="px-4 py-3.5 text-[14px] border-b border-white/[0.08] text-[#a1a1a6]">{a.dates}</td>
                  <td className="px-4 py-3.5 text-[14px] border-b border-white/[0.08]">{a.price} ₽</td>
                  <td className="px-4 py-3.5 border-b border-white/[0.08]">
                    <Badge variant={s.variant}>{s.label}</Badge>
                  </td>
                  <td className="px-4 py-3.5 border-b border-white/[0.08]">
                    {a.status === 'pending' && (
                      <button className="text-[13px] text-[#a1a1a6] hover:text-[#ff453a] transition-colors cursor-pointer bg-transparent border-none font-[inherit]">
                        Отозвать
                      </button>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}