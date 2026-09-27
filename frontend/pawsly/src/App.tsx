import { Routes, Route } from 'react-router-dom'
import Layout from '@/components/layout/Layout'
import Home from '@/pages/Home'
import MyPets from '@/pages/MyPets'
import MyListings from '@/pages/MyListings'
import MyApplications from '@/pages/MyApplications'
import MyBookings from '@/pages/MyBookings'
import Wallet from '@/pages/Wallet'
import Profile from '@/pages/Profile'
import Login from '@/pages/Login'
import Register from '@/pages/Register'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/my-pets" element={<MyPets />} />
        <Route path="/my-listings" element={<MyListings />} />
        <Route path="/my-applications" element={<MyApplications />} />
        <Route path="/my-bookings" element={<MyBookings />} />
        <Route path="/wallet" element={<Wallet />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
    </Routes>
  )
}