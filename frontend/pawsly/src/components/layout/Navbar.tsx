import { useNavigate, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui'

const links = [
  { path: '/', label: 'Найти ситтера' },
  { path: '/my-pets', label: 'Питомцы' },
  { path: '/my-listings', label: 'Объявления' },
  { path: '/my-applications', label: 'Заявки' },
  { path: '/my-bookings', label: 'Бронирования' },
]

export default function Navbar() {
  const navigate = useNavigate()
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 h-[52px] bg-[#0a0a0a]/85 backdrop-blur-xl border-b border-white/[0.08] flex items-center px-6 gap-2 z-50">
      <div
        className="text-[17px] font-semibold cursor-pointer mr-2"
        onClick={() => navigate('/')}
      >
        Paws<span className="text-[#5e9bff]">ly</span>
      </div>

      <div className="flex gap-0.5 flex-1">
        {links.map(link => (
          <button
            key={link.path}
            onClick={() => navigate(link.path)}
            className={[
              'px-3 py-1.5 rounded-lg text-[13px] transition-all duration-150 cursor-pointer border-none bg-transparent font-[inherit] whitespace-nowrap',
              pathname === link.path
                ? 'text-[#f5f5f7] bg-[#1c1c1e]'
                : 'text-[#a1a1a6] hover:text-[#f5f5f7] hover:bg-[#1c1c1e]',
            ].join(' ')}
          >
            {link.label}
          </button>
        ))}
      </div>

      <div className="flex gap-2 items-center ml-auto">
        <Button size="sm" onClick={() => navigate('/wallet')}>💳 Кошелёк</Button>
        <Button size="sm" onClick={() => navigate('/profile')}>Профиль</Button>
      </div>
    </nav>
  )
}