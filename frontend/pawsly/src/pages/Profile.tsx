import { useState } from 'react'
import { Button, FormGroup, Input } from '@/components/ui'

export default function Profile() {
  const [username, setUsername] = useState('denis_ivan')
  const [email, setEmail] = useState('denis@example.com')
  const [saved, setSaved] = useState(false)

  function save() {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex gap-5 items-center mb-8">
        <div className="w-[72px] h-[72px] rounded-full bg-[#1c1c1e] flex items-center justify-center text-[32px] flex-shrink-0">
          😊
        </div>
        <div>
          <div className="text-[22px] font-semibold">{username}</div>
          <div className="text-[14px] text-[#a1a1a6] mt-1">Владелец животных</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6 max-[600px]:grid-cols-1">
        {[
          { label: 'Объявлений создано', value: '4' },
          { label: 'Бронирований', value: '7' },
        ].map(s => (
          <div key={s.label} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5">
            <div className="text-[13px] text-[#a1a1a6] mb-2">{s.label}</div>
            <div className="text-[28px] font-semibold tracking-tight">{s.value}</div>
          </div>
        ))}
      </div>

      <div className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5">
        <div className="text-[13px] font-medium text-[#636366] uppercase tracking-wider mb-4">
          Личные данные
        </div>
        <FormGroup label="Имя пользователя">
          <Input value={username} onChange={e => setUsername(e.target.value)} />
        </FormGroup>
        <FormGroup label="Email">
          <Input type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </FormGroup>
        <Button variant="primary" onClick={save}>
          {saved ? '✓ Сохранено' : 'Сохранить'}
        </Button>
      </div>
    </div>
  )
}