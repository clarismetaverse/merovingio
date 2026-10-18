import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import GenericSpacesExplorer from './GenericSpacesExplorer'
import './generic-spaces.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <GenericSpacesExplorer />
  </StrictMode>,
)
