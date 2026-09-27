import React from 'react'
import { clsx } from 'clsx'

type ButtonVariant = 'primary' | 'ghost' | 'danger'
type ButtonSize = 'sm' | 'md'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
}

const buttonStyles: Record<ButtonVariant, string> = {
  primary: 'bg-[#5e9bff] text-white hover:bg-[#4a87f0]',
  ghost: 'bg-[#1c1c1e] text-[#f5f5f7] hover:bg-[#2c2c2e]',
  danger: 'bg-red-500/10 text-[#ff453a] hover:bg-red-500/20',
}

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-[13px]',
  md: 'px-4 py-2 text-[14px]',
}

export function Button({ variant = 'ghost', size = 'md', className, children, ...props }: ButtonProps) {
  return (
    <button
      className={clsx(
        'inline-flex items-center gap-1.5 rounded-lg font-medium transition-all duration-150 border-none cursor-pointer font-[inherit]',
        buttonStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

type BadgeVariant = 'green' | 'blue' | 'yellow' | 'red' | 'gray'

const badgeStyles: Record<BadgeVariant, string> = {
  green: 'bg-green-500/15 text-[#30d158]',
  blue: 'bg-blue-500/15 text-[#5e9bff]',
  yellow: 'bg-yellow-500/15 text-[#ffd60a]',
  red: 'bg-red-500/15 text-[#ff453a]',
  gray: 'bg-[#1c1c1e] text-[#a1a1a6]',
}

export function Badge({ variant = 'gray', children }: { variant?: BadgeVariant; children: React.ReactNode }) {
  return (
    <span className={clsx('inline-flex items-center px-2 py-0.5 rounded-md text-[12px] font-medium', badgeStyles[variant])}>
      {children}
    </span>
  )
}

export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={clsx('bg-[#141414] border border-white/[0.08] rounded-[18px] overflow-hidden', className)}>
      {children}
    </div>
  )
}

export function CardBody({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={clsx('p-5', className)}>{children}</div>
}

export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={clsx(
        'w-full px-3.5 py-2.5 bg-[#1c1c1e] border border-white/[0.08] rounded-xl text-[#f5f5f7] text-[14px] font-[inherit] outline-none transition-colors focus:border-[#5e9bff] placeholder:text-[#636366]',
        className
      )}
      {...props}
    />
  )
}

export function Select({ className, children, ...props }: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={clsx(
        'w-full px-3.5 py-2.5 bg-[#1c1c1e] border border-white/[0.08] rounded-xl text-[#f5f5f7] text-[14px] font-[inherit] outline-none transition-colors focus:border-[#5e9bff] cursor-pointer',
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
}

export function Textarea({ className, ...props }: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={clsx(
        'w-full px-3.5 py-2.5 bg-[#1c1c1e] border border-white/[0.08] rounded-xl text-[#f5f5f7] text-[14px] font-[inherit] outline-none transition-colors focus:border-[#5e9bff] placeholder:text-[#636366] resize-none',
        className
      )}
      {...props}
    />
  )
}

export function FormGroup({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mb-4">
      <label className="block text-[13px] text-[#a1a1a6] mb-1.5">{label}</label>
      {children}
    </div>
  )
}

export function Modal({ open, onClose, title, children }: {
  open: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}) {
  if (!open) return null
  return (
    <div
      className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-6"
      onClick={e => { if (e.target === e.currentTarget) onClose() }}
    >
      <div className="bg-[#141414] border border-white/[0.08] rounded-[18px] w-full max-w-[440px] p-7">
        <div className="text-[18px] font-semibold mb-5">{title}</div>
        {children}
      </div>
    </div>
  )
}

export function ModalFooter({ children }: { children: React.ReactNode }) {
  return <div className="flex gap-2 justify-end mt-5">{children}</div>
}

export function Divider() {
  return <div className="h-px bg-white/[0.08] my-5" />
}

export function EmptyState({ icon, title, text, action }: {
  icon: string
  title: string
  text: string
  action?: React.ReactNode
}) {
  return (
    <div className="text-center py-16 px-6 text-[#a1a1a6]">
      <div className="text-5xl mb-4">{icon}</div>
      <div className="text-[17px] font-medium text-[#f5f5f7] mb-2">{title}</div>
      <div className="text-[14px] mb-6">{text}</div>
      {action}
    </div>
  )
}