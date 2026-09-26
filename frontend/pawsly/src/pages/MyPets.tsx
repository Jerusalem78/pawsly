import { useState } from 'react'
import { Button, Modal, ModalFooter, FormGroup, Input, Select, Textarea } from '@/components/ui'
import type { Pet } from '@/types'

const DEMO_PETS: Pet[] = [
  { id: '1', owner_id: 'me', name: 'Бобик', species: 'dog', breed: 'Лабрадор', age: 3, special_notes: 'Аллергия на курицу', is_active: true },
  { id: '2', owner_id: 'me', name: 'Мурка', species: 'cat', breed: 'Мейн-кун', age: 5, special_notes: 'Боится собак', is_active: true },
]

const EMOJI: Record<string, string> = {
  dog: '🐶', cat: '🐱', bird: '🐦', rodent: '🐹', reptile: '🦎', other: '🐾',
}

export default function MyPets() {
  const [pets, setPets] = useState<Pet[]>(DEMO_PETS)
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [species, setSpecies] = useState('dog')
  const [breed, setBreed] = useState('')
  const [age, setAge] = useState('')
  const [notes, setNotes] = useState('')

  function addPet() {
    setPets(p => [...p, { id: Date.now().toString(), owner_id: 'me', name, species: species as Pet['species'], breed, age: Number(age), special_notes: notes, is_active: true }])
    setOpen(false)
    setName(''); setBreed(''); setAge(''); setNotes('')
  }

  function removePet(id: string) {
    setPets(p => p.filter(x => x.id !== id))
  }

  return (
    <div className="max-w-[960px] mx-auto px-6 py-8">
      <div className="flex items-start justify-between mb-7">
        <div>
          <h1 className="text-[26px] font-semibold tracking-tight">Мои питомцы</h1>
          <p className="text-[14px] text-[#a1a1a6] mt-1">Управляйте профилями ваших животных</p>
        </div>
        <Button variant="primary" onClick={() => setOpen(true)}>+ Добавить</Button>
      </div>

      {pets.length === 0 ? (
        <div className="text-center py-16 text-[#a1a1a6]">
          <div className="text-5xl mb-4">🐾</div>
          <div className="text-[17px] font-medium text-[#f5f5f7] mb-2">Нет питомцев</div>
          <div className="text-[14px] mb-6">Добавьте первого питомца чтобы создавать объявления</div>
          <Button variant="primary" onClick={() => setOpen(true)}>Добавить питомца</Button>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 max-[600px]:grid-cols-1">
          {pets.map(pet => (
            <div key={pet.id} className="bg-[#141414] border border-white/[0.08] rounded-[18px] p-5 flex gap-4">
              <div className="w-[52px] h-[52px] bg-[#1c1c1e] rounded-full flex items-center justify-center text-2xl flex-shrink-0">
                {EMOJI[pet.species]}
              </div>
              <div className="flex-1">
                <div className="text-[15px] font-medium">{pet.name}</div>
                <div className="text-[13px] text-[#a1a1a6] mt-0.5">
                  {pet.breed ? `${pet.breed} · ` : ''}{pet.age} {pet.age === 1 ? 'год' : 'лет'}
                </div>
                {pet.special_notes && (
                  <div className="text-[12px] text-[#636366] mt-1">{pet.special_notes}</div>
                )}
                <div className="flex gap-1.5 mt-3">
                  <Button size="sm">Изменить</Button>
                  <Button size="sm" variant="danger" onClick={() => removePet(pet.id)}>Удалить</Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal open={open} onClose={() => setOpen(false)} title="Добавить питомца">
        <FormGroup label="Кличка">
          <Input placeholder="Бобик" value={name} onChange={e => setName(e.target.value)} />
        </FormGroup>
        <FormGroup label="Вид">
          <Select value={species} onChange={e => setSpecies(e.target.value)}>
            <option value="dog">🐶 Собака</option>
            <option value="cat">🐱 Кошка</option>
            <option value="bird">🐦 Птица</option>
            <option value="rodent">🐹 Грызун</option>
            <option value="reptile">🦎 Рептилия</option>
            <option value="other">🐾 Другое</option>
          </Select>
        </FormGroup>
        <FormGroup label="Порода">
          <Input placeholder="Лабрадор" value={breed} onChange={e => setBreed(e.target.value)} />
        </FormGroup>
        <FormGroup label="Возраст (лет)">
          <Input type="number" placeholder="3" value={age} onChange={e => setAge(e.target.value)} />
        </FormGroup>
        <FormGroup label="Особые пометки">
          <Textarea rows={2} placeholder="Аллергии, особенности..." value={notes} onChange={e => setNotes(e.target.value)} />
        </FormGroup>
        <ModalFooter>
          <Button onClick={() => setOpen(false)}>Отмена</Button>
          <Button variant="primary" onClick={addPet}>Сохранить</Button>
        </ModalFooter>
      </Modal>
    </div>
  )
}