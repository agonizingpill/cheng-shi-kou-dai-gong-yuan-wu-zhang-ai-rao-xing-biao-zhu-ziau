from domain.entrances_api import router as entrances
from domain.walk_profiles_api import router as walk_profiles
from domain.detours_api import router as detours
from domain.map_notes_api import router as map_notes
from domain.trials_api import router as trials

routers = (entrances, walk_profiles, detours, map_notes, trials,)
