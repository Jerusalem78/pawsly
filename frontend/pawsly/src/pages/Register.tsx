import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, FormGroup, Input, Select } from '@/components/ui'
import { validateAuth } from '@/features/auth/lib/validation'
import { FieldError } from '@/shared/ui/FieldError'
import { writeStorage } from '@/shared/lib/storage'

export default function Register() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('owner')
  const [errors, setErrors] = useState<Record<string, string>>({})
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const next = validateAuth({ username, email, password }, true)
    setErrors(next)
    if (Object.keys(next).length) return
    writeStorage('pawsly-session', { username: username.trim(), email, role })
    navigate('/')
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-9 w-full max-w-[380px]">
        <div className="text-[22px] font-semibold mb-1.5">Регистрация</div>
        <div className="text-[14px] text-[#a1a1a6] mb-7">Создайте аккаунт в Pawsly</div>

        <form onSubmit={submit} noValidate>
        <FormGroup label="Имя пользователя">
          <Input required autoComplete="username" placeholder="ivan_petrov" value={username} onChange={e => setUsername(e.target.value)} />
          <FieldError>{errors.username}</FieldError>
        </FormGroup>
        <FormGroup label="Email">
          <Input type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} />
          <FieldError>{errors.email}</FieldError>
        </FormGroup>
        <FormGroup label="Пароль">
          <Input type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} />
          <FieldError>{errors.password}</FieldError>
        </FormGroup>
        <FormGroup label="Роль">
          <Select value={role} onChange={e => setRole(e.target.value)}>
            <option value="owner">Владелец животного</option>
            <option value="sitter">Ситтер</option>
          </Select>
        </FormGroup>

        <Button type="submit" variant="primary" className="w-full justify-center mt-2">
          Создать аккаунт
        </Button>

        <div className="text-center text-[13px] text-[#a1a1a6] mt-5">
          Уже есть аккаунт?{' '}
          <span className="text-[#5e9bff] cursor-pointer" onClick={() => navigate('/login')}>
            Войти
          </span>
        </div>
        </form>
      </div>
    </div>
  )
}
