# Game Design Document (GDD)

## Buildings (aka. Establishments) (abbr: bd)

* Throne | Castle | City Hall | Kingdom | Food | Population
	* controls the max of all other bd

* Production | Workshop | Workers | Bank(?)
	* controls new spawn face value

* Science | Academy | School | College | Library
	* controls the max of mt units

* Culture | Museum | Civic Center 
	* controls the max of tile face value

* Religion | Temple | Shine | Prophet
	* can be higher than Throne
	* when that happens, double new spawn face value
	* when that happens, chance double merged tiles
	* when that happens, chance more than one new spawn


## Millitary unit (abbr: mt)
* when it matches the enemy value, kills it
* keeps there, will not remove
* with chance being halved if too long with enemy
* enemy attack: with a clock counter
* when enemy attach happend. both or just player got halved

## Win condition
* Millitary: beat the last wave of aliens 


## Lose condition
* If cannot move tiles (any or more of there): 
	* 1/2 of all bd
	* 1/2 of all mt
	* remove (3) largest tiles
* HP or chances 
	* 3 Lives
	* cannot move, then take one off
* No read Game Over condition, like idle games
* Lose when cannot kill enemy wave when counter down


## Civs
* China		large population bonus (throne merge auto x2)
* USA		Production unlimited
* Russia	Wave counter + 1
* Arabia	Regilion always Throne * 2
* France	Culture unlimited
* Japan		Mil can take bigger enemy
* Egypt		Build wonders 50% faster / Regilion always Culture * 4
* India		large populatoin bonus (throne merge auto x2)

## Wonders
* TBD
* TBD


## Misc. Design
* 4x4 only. otherwise too easy
* 5x5. its ok to be too easy. it's about build your empire
