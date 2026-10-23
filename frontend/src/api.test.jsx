import {describe,it,expect} from 'vitest';
describe('marketplace frontend starter',()=>{it('uses a local identity service default',()=>{expect(import.meta.env.VITE_IDENTITY_URL||'http://localhost:8001').toContain('localhost:8001')})})
