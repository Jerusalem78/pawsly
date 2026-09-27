import { useState } from 'react'
import { Button, Modal, ModalFooter, FormGroup, Input } from '@/components/ui'

const TRANSACTIONS = [
  { id: '1', type: 'Пополнение', amount: 3000, sign: '+', color: '#30d158', date: '10 июля' },
  { id: '2', type: 'Заморозка (эскроу)', amount: 2500, sign: '-', color: '#ffd60a', date: '14 июля' },
  { id: '3', type: 'Выплата ситтеру', amount: 1500, sign: '-', color: '#ff453a', date: '6 июня' },
  { id: '4', type: 'Пополнение', amount: 6200, sign: '+', color: '#30d158', date: '1 июня' },
]

export default function Wallet() {
  const [open, setOpen] = useState(false)
  const [amount, setAmount] = useState('')

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="mb-7">
        <h1 className="text-[26px] font-semibold tracking-tight">Кошелёк</h1>
      </div>

      <div className="rounded-[18px] border border-[rgba(94,155,255,0.2)] p-8 mb-6 text-center"
        style={{ background: 'linear-gradient(135deg, #1a2744 0%, #1c1c2e 100%)' }}>
        <div className="text-[13px] text-[#a1a1a6] mb-2">Доступный баланс</div>
        <div className="text-[42px] font-light tracking-[-2px]">5 200 ₽</div>
        <div className="text-[13px] text-[#636366] mt-2">800 ₽ в эскроу</div>
        <div className="mt-5">
          <Button variant="primary" onClick={() => setOpen(true)}>Пополнить</Button>
        </div>
      </div>

      <div className="text-[13px] font-medium text-[#636366] uppercase tracking-wider mb-3">
        История транзакций
      </div>

      <div className="bg-[#141414] border border-white/[0.08] rounded-[18px] overflow-hidden">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              {['Тип', 'Сумма', 'Дата'].map(h => (
                <th key={h} className="text-left text-[12px] font-medium text-[#636366] px-4 py-2.5 border-b border-white/[0.08] uppercase tracking-wide">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {TRANSACTIONS.map(t => (
              <tr key={t.id} className="hover:[&>td]:bg-[#1c1c1e]">
                <td className="px-4 py-3.5 text-[14px] border-b border-white/[0.08]">{t.type}</td>
                <td className="px-4 py-3.5 text-[14px] font-medium border-b border-white/[0.08]"
                  style={{ color: t.color }}>
                  {t.sign}{t.amount} ₽
                </td>
                <td className="px-4 py-3.5 text-[14px] text-[#a1a1a6] border-b border-white/[0.08]">{t.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal open={open} onClose={() => setOpen(false)} title="Пополнить кошелёк">
        <FormGroup label="Сумма (₽)">
          <Input type="number" placeholder="1000" value={amount} onChange={e => setAmount(e.target.value)} />
        </FormGroup>
        <ModalFooter>
          <Button onClick={() => setOpen(false)}>Отмена</Button>
          <Button variant="primary" onClick={() => setOpen(false)}>Пополнить</Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}