import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import WorkspaceAtlasPrototype from './WorkspaceAtlasPrototype'
import './workspace-atlas.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <WorkspaceAtlasPrototype />
  </StrictMode>,
)
