import sys
import math

def make_blanket( blanket_radius, blanket_width, blanket_height, shell_thickness ):        
    cubit.cmd( f"create brick x {blanket_height} y {blanket_width} z {blanket_width}" )
    shell_volume_id = cubit.get_last_id( "volume" )
    cubit.cmd( f"modify curve {get_closest_curve_in_volume_to_location( shell_volume_id, (blanket_height/2, blanket_width/2, 0) )} blend radius {blanket_radius}" )
    cubit.cmd( f"modify curve {get_closest_curve_in_volume_to_location( shell_volume_id, (-blanket_height/2, blanket_width/2, 0) )} blend radius {blanket_radius}" )

    cubit.cmd( f"create sheet offset from surface in vol {shell_volume_id} offset {-1*shell_thickness} " )
    inner_volume_id = cubit.get_last_id( "volume" )

    before_vol_ids = cubit.get_entities( "volume" )
    cubit.cmd( f"subtract volume {inner_volume_id} from volume {shell_volume_id} keep_tool" )
    after_vol_ids = cubit.get_entities( "volume" )
    inner_volume_id, shell_volume_id = get_operation_return_ids( before_vol_ids, after_vol_ids )
    
    cubit.cmd( f"block 1 volume {cubit.get_id_string( shell_volume_id )}" )
    cubit.cmd( f"block 2 volume {cubit.get_id_string( inner_volume_id )}" )
    cubit.cmd( "block 1 name 'OuterShell'" )
    cubit.cmd( "block 2 name 'InnerVolume'" )

def get_closest_curve_in_volume_to_location( vol_id, location ):
    C = cubit.parse_cubit_list( "curve", f"in volume {vol_id}" )
    min_dist = float( "inf" )
    for cid in C:
        curve = cubit.curve(cid)
        curve_close_point = curve.closest_point_trimmed( location )
        dist = math.sqrt( ( location[0] - curve_close_point[0] )**2 + ( location[1] - curve_close_point[1] )**2  + ( location[2] - curve_close_point[2] )**2 )
        if dist < min_dist:
            min_dist = dist
            closest_curve_id = cid
    return closest_curve_id

def get_operation_return_ids( before_ids, after_ids ):
    persist_ids = []
    for id in before_ids:
        if id in after_ids:
            persist_ids.append( id )
    return_ids = []
    for id in after_ids:
        if id > before_ids[-1]:
            return_ids.append( id )
    return ( persist_ids, return_ids )

def main():
    make_blanket( blanket_radius = 5, blanket_width = 40, blanket_height = 100, shell_thickness = 1 )
    cubit.cmd("save as 'test.cub5' overwrite")
    
## Start Cubit
if __name__ == "__main__":
    sys.path.append('/opt/Coreform-Cubit-2023.8/bin/')
    import cubit
    cubit.init(['cubit', '-journalfile', 'try_greg_history.jou'])
    cubit.cmd( "reset" )
    main()
elif __name__ == "__coreformcubit__":
    cubit.cmd( "reset" )
    main()