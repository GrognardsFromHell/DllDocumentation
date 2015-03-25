from toee import *

def OnBeginSpellCast( spell ):
	print "Scorching Ray OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	game.particles( "sp-conjuration-conjure", spell.caster )

def OnSpellEffect( spell ):
	print "Scorching Ray OnSpellEffect"

def OnBeginProjectile( spell, projectile, index_of_target ):
	print "Scorching Ray OnBeginProjectile"

	projectiles = min(3, (spell.caster_level + 1) / 4)
	if index_of_target < projectiles:
		projectile.obj_set_int( obj_f_projectile_part_sys_id, game.particles( 'sp-Scorching Ray', projectile ) )

def OnEndProjectile( spell, projectile, index_of_target ):
	print "Scorching Ray OnEndProjectile"

	projectiles = min(3, (spell.caster_level + 1) / 4)
	if index_of_target < projectiles:
		damage_dice = dice_new( '4d6' )

		spell.duration = 0

		game.particles_end( projectile.obj_get_int( obj_f_projectile_part_sys_id ) )

		target = spell.target_list[ index_of_target ]

		return_val = spell.caster.perform_touch_attack( target.obj )
		if return_val == 1:

			game.particles( 'sp-Scorching Ray-Hit', target.obj )
			target.obj.spell_damage( spell.caster, D20DT_FIRE, damage_dice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id )

		elif return_val == 2:

			game.particles( 'sp-Scorching Ray-Hit', target.obj )

			# critical hit
			damage_dice.num = 2
			target.obj.spell_damage( spell.caster, D20DT_FIRE, damage_dice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id )

		else:

			# missed
			target.obj.float_mesfile_line( 'mes\\spell.mes', 30007 )

			game.particles( 'Fizzle', target.obj )

	spell.num_of_projectiles = spell.num_of_projectiles - 1
	if ( spell.num_of_projectiles == 0 ):
		spell.spell_end( spell.id, 1 )

def OnEndSpellCast( spell ):
	print "Scorching Ray OnEndSpellCast"