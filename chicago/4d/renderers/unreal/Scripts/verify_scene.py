"""Editor-side structural checks. These do not substitute for a packaged play test."""
import json
import os
from pathlib import Path
import unreal

out = Path(os.environ['CHICAGO_PROJECT']) / 'Scripts'
report = json.loads((out/'import_report.json').read_text())
levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.load_level(report['level']), 'Map did not load'
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
owned = [actor for actor in actors if unreal.Name('Chicago4D') in actor.tags]
expected = sum(row['mesh_count'] for row in report['imported'])
assert len(owned) == expected, (len(owned), expected)
for actor in owned:
    component = actor.static_mesh_component
    if actor.get_actor_label() == 'water':
        assert str(component.get_collision_profile_name()) == 'NoCollision'
    else:
        body = component.static_mesh.get_editor_property('body_setup')
        assert body.get_editor_property('collision_trace_flag') == unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
        assert str(component.get_collision_profile_name()) == 'BlockAll'
world = unreal.EditorLevelLibrary.get_editor_world()
mode = world.get_world_settings().get_editor_property('default_game_mode')
assert mode == unreal.load_class(None, '/Script/Chicago4D.ChicagoGameMode')
pawn = unreal.get_default_object(mode).get_editor_property('default_pawn_class')
assert pawn == unreal.load_class(None, '/Script/Chicago4D.ChicagoWalker')
starts = [a for a in actors if isinstance(a, unreal.PlayerStart)]
assert len(starts) == 1
assert not report['errors']
(out/'verification.json').write_text(json.dumps({
    'imported_mesh_actors': len(owned), 'solid_and_water_collision_profiles': 'pass',
    'native_body_free_pawn': 'pass', 'player_start_count': len(starts),
    'source_commit': report['source_commit'], 'play_test': 'Required separately'
}, indent=2)+'\n')
unreal.log('CHICAGO_VERIFY_PASS')
