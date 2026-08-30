'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { initializeApp, getApps, FirebaseApp } from 'firebase/app'
import { getAuth, Auth, onAuthStateChanged, User, signInWithPopup, GoogleAuthProvider, signOut } from 'firebase/auth'

const firebaseConfig = {
  apiKey: "AIzaSyDub3ETgYZm333Tw6V3ME_9sDIpNgWaIus",
  authDomain: "jarvis-ai-3ba39.firebaseapp.com",
  projectId: "jarvis-ai-3ba39",
  storageBucket: "jarvis-ai-3ba39.firebasestorage.app",
  messagingSenderId: "63810563265",
  appId: "1:63810563265:web:0a570af6ab49c8ec673840",
  measurementId: "G-XVZDDQWXB2"
}

let app: FirebaseApp
let auth: Auth
let googleProvider: GoogleAuthProvider

if (typeof window !== 'undefined') {
  if (!getApps().length) {
    app = initializeApp(firebaseConfig)
  } else {
    app = getApps()[0]
  }
  auth = getAuth(app)
  googleProvider = new GoogleAuthProvider()
}

interface AuthContextType {
  user: User | null
  loading: boolean
  signIn: () => Promise<void>
  signOutUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  signIn: async () => {},
  signOutUser: async () => {},
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!auth) {
      setLoading(false)
      return
    }
    const unsubscribe = onAuthStateChanged(auth, (u) => {
      setUser(u)
      setLoading(false)
    })
    return () => unsubscribe()
  }, [])

  const signIn = async () => {
    if (!auth || !googleProvider) {
      console.warn('Firebase not configured')
      return
    }
    try {
      await signInWithPopup(auth, googleProvider)
    } catch (error) {
      console.error('Sign-in failed', error)
    }
  }

  const signOutUser = async () => {
    if (!auth) return
    await signOut(auth)
  }

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signOutUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
