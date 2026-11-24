'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { displayNameSchema } from '@/types/auth/profile';

export function DisplayNameForm({ initialName }: { initialName: string }) {
  const [name, setName] = useState(initialName);
  const [message, setMessage] = useState('');
  const router = useRouter();
  return <form onSubmit={async event => {
    event.preventDefault();
    if (!displayNameSchema.safeParse(name).success) { setMessage('Invalid display name'); return; }
    const response = await fetch('/api/profile/display-name', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name }),
    });
    if (response.ok) { setName(name.trim()); setMessage('Saved'); router.refresh(); }
    else setMessage('Invalid display name');
  }}>
    <label htmlFor="display-name">Display name</label>
    <input id="display-name" name="name" value={name} onChange={e => setName(e.target.value)} />
    <button type="submit">Save name</button><p role="status">{message}</p>
  </form>;
}
