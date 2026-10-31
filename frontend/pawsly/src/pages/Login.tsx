import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button, FormGroup, Input } from '@/components/ui'
import { validateAuth } from '@/features/auth/lib/validation'
import { FieldError } from '@/shared/ui/FieldError'
import { writeStorage } from '@/shared/lib/storage'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const errors = validateAuth({ email, password })
    if (Object.keys(errors).length) { setError(errors.email ?? errors.password ?? 'Проверьте поля'); return }
    writeStorage('pawsly-session', { email, username: email.split('@')[0] })
    navigate('/')
  }

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="max-w-[400px] mx-auto mt-12 bg-[#141414] border border-white/[0.08] rounded-[18px] p-8">
        <h1 className="text-[24px] font-semibold mb-1">Вход</h1><p className="text-sm text-[#a1a1a6] mb-6">Войдите в свой аккаунт Pawsly</p>
        <form onSubmit={submit} noValidate>
          <FormGroup label="Email"><Input type="email" autoComplete="email" value={email} onChange={e => setEmail(e.target.value)} aria-invalid={!!error} /></FormGroup>
          <FormGroup label="Пароль"><Input type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} /></FormGroup>
          {error && <p role="alert" className="text-sm text-[#ff6961] mb-3">{error}</p>}
          <Button type="submit" variant="primary" className="w-full justify-center">Войти</Button>
        </form>
        <p className="text-center text-sm text-[#a1a1a6] mt-5">Нет аккаунта? <Link className="text-[#5e9bff]" to="/register">Зарегистрироваться</Link></p>
      </div>
    </div>
  )
}
