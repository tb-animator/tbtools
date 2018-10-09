import tb_pickwalk_setup as tbpw
from tb_pickwalk_setup import pickInfo
reload(tbpw)

'''
Here's an example template from one of my personal rigs for pickwalking setup
pick_data is a list of 'pickInfo' objects, which in turn contain a control,
and the objects for each of the 4 pick directions
the sides dict is used so you only need to set up one side of the rig

'fingers' is used to quickly set up a set of fingers, so the pickwalk will
loop around from pinky back to thumb, and so you don't have to set up each individual digit.
This can be used for hair and other misc body parts
'''

pick_data = []
sides = { "left" : ["l","r"], "right" : ["r", "l"] }
rig_sides = [ "left", "right"]

##################
# fk fingers (5) #
##################
fingers = ['thumb',
           'index',
           'middle',
           'ring',
           'pinky']
digit_length = 3

for side in rig_sides:
    both_sides = sides[side]
    this_side = both_sides[0]
    o_side = both_sides[1]

    ################
    # fk limb -arm #
    ################

    # shoulder
    pick_data.append(pickInfo(control="driver_%s_shoulder" % this_side,
                              up="torso_ctrl",
                              down="driver_%s_arm" % this_side,
                              left="driver_%s_shoulder" % o_side,
                              right="driver_%s_shoulder" % o_side))
    # arm
    pick_data.append(pickInfo(control="driver_%s_arm" % this_side,
                              up="driver_%s_shoulder" % this_side,
                              down="driver_%s_elbow" % this_side,
                              left="driver_%s_arm" % o_side,
                              right="driver_%s_arm" % o_side))
    # elbow
    pick_data.append(pickInfo(control="driver_%s_elbow" % this_side,
                              up="driver_%s_arm" % this_side,
                              down="driver_%s_wrist" % this_side,
                              left="driver_%s_elbow" % o_side,
                              right="driver_%s_elbow" % o_side))
    # wrist
    pick_data.append(pickInfo(control="driver_%s_wrist" % this_side,
                              up="driver_%s_elbow" % this_side,
                              down="driver_%s_index_00" % this_side,
                              left="driver_%s_wrist" % o_side,
                              right="driver_%s_wrist" % o_side))
    ################
    # ik limb -arm #
    ################

    # ik foot
    pick_data.append(pickInfo(control="%s_arm_ctrl" % this_side,
                              up="torso_ctrl",
                              down="%s_arm_PV_ctrl" % this_side,
                              left="%s_arm_ctrl" % o_side,
                              right="%s_arm_ctrl" % o_side))
    # ik foot pivot
    pick_data.append(pickInfo(control="%s_arm_PV_ctrl" % this_side,
                              up="%s_arm_ctrl" % this_side,
                              down="%s_foot_pivot_ctrl" % this_side,
                              left="%s_arm_PV_ctrl" % o_side,
                              right="%s_arm_PV_ctrl" % o_side))


    ################
    # fk limb -leg #
    ################

    # thigh
    pick_data.append(pickInfo(control="driver_%s_leg" % this_side,
                              up="hips_ctrl",
                              down="driver_%s_knee" % this_side,
                              left="driver_%s_leg" % o_side,
                              right="driver_%s_leg" % o_side))
    # knee
    pick_data.append(pickInfo(control="driver_%s_knee" % this_side,
                              up="driver_%s_leg" % this_side,
                              down="driver_%s_ankle" % this_side,
                              left="driver_%s_knee" % o_side,
                              right="driver_%s_knee" % o_side))
    # ankle
    pick_data.append(pickInfo(control="driver_%s_ankle" % this_side,
                              up="driver_%s_knee" % this_side,
                              down="driver_%s_ball" % this_side,
                              left="driver_%s_ankle" % o_side,
                              right="driver_%s_ankle" % o_side))
    # ball
    pick_data.append(pickInfo(control="driver_%s_ball" % this_side,
                              up="driver_%s_ankle" % this_side,
                              down="driver_%s_ball" % this_side,
                              left="driver_%s_ball" % o_side,
                              right="driver_%s_ball" % o_side))
    ################
    # ik limb -leg #
    ################

    # ik foot
    pick_data.append(pickInfo(control="%s_leg_ctrl" % this_side,
                              up="driver_root",
                              down="%s_foot_pivot_ctrl" % this_side,
                              left="%s_leg_ctrl" % o_side,
                              right="%s_leg_ctrl" % o_side))
    # ik foot pivot
    pick_data.append(pickInfo(control="%s_foot_pivot_ctrl" % this_side,
                              up="%s_leg_ctrl" % this_side,
                              down="%s_foot_pivot_ctrl" % this_side,
                              left="%s_foot_pivot_ctrl" % o_side,
                              right="%s_foot_pivot_ctrl" % o_side))
    # ik foot pivot
    pick_data.append(pickInfo(control="%s_leg_PV_ctrl" % this_side,
                              up="%s_foot_pivot_ctrl" % this_side,
                              down="%s_leg_PV_ctrl" % this_side,
                              left="%s_leg_PV_ctrl" % o_side,
                              right="%s_leg_PV_ctrl" % o_side))



    length = len(fingers)
    for digits in fingers:
        # thumb 00
        current_index = fingers.index(digits)
        left_digit = fingers[(current_index -1) % length]
        right_digit = fingers[(current_index +1) % length]
        for j in range(0,digit_length):
            parent_control = ["driver_%s_%s_0%s" % (this_side,digits, j-1), "driver_%s_wrist" % this_side ]
            pick_data.append(pickInfo(control="driver_%s_%s_0%s" % (this_side,digits, j),
                                      up=parent_control[j == 0],
                                      down="driver_%s_%s_0%s" % (this_side, digits, min(j+1, digit_length-1)),
                                      left="driver_%s_%s_0%s" % (this_side, left_digit, j),
                                      right="driver_%s_%s_0%s" % (this_side, right_digit, j)))

    # palm joint #
    pick_data.append(pickInfo(control="driver_%s_palm_pinky" % this_side,
                              up="driver_%s_wrist" % this_side,
                              down="driver_%s_pinky_00" % this_side,
                              left="driver_%s_thumb_00" % o_side,
                              right="driver_%s_thumb_00" % o_side))
    pick_data.append(pickInfo(control="driver_%s_pinky_00" % this_side,
                              up="driver_%s_palm_pinky" % this_side))

'''
    #################
    # flaps controls #
    #################
    _length = 4
    for i in range(0, _length):
        parent_control = ["driver_%s_flap_0%s" % (this_side, i-1), "cog_ctrl" ]
        pick_data.append(pickInfo(control="driver_%s_flap_0%s" % (this_side, i),
                          up=parent_control[i == 0],
                          down="driver_%s_flap_0%s" % (this_side, min(i+1, _length-1)),
                          left="driver_%s_flap_0%s" % (o_side, i),
                          right="driver_%s_flap_0%s" % (o_side, i)))
'''
###################
# centre controls #
###################

# global_root
pick_data.append(pickInfo(control="global_root",
                          up="global_root",
                          down="driver_root",
                          left="export_root",
                          right="export_root"))
# driver_root
pick_data.append(pickInfo(control="driver_root",
                          up="global_root",
                          down="cog_ctrl",
                          left="export_root",
                          right="export_root"))
# cog_ctrl
pick_data.append(pickInfo(control="cog_ctrl",
                          up="driver_root",
                          down="hips_ctrl",
                          left="driver_l_leg",
                          right="driver_r_leg"))
# hips_ctrl
pick_data.append(pickInfo(control="hips_ctrl",
                          up="cog_ctrl",
                          down="gut_ctrl",
                          left="driver_l_leg",
                          right="driver_r_leg"))
# gut_ctrl
pick_data.append(pickInfo(control="gut_ctrl",
                          up="hips_ctrl",
                          down="torso_ctrl",
                          left="gut_ctrl",
                          right="gut_ctrl"))
# torso_ctrl
pick_data.append(pickInfo(control="torso_ctrl",
                          up="gut_ctrl",
                          down="head_ctrl",
                          left="driver_l_shoulder",
                          right="driver_r_shoulder"))
'''
# head_ctrl
pick_data.append(pickInfo(control="head_ctrl",
                          up="torso_ctrl",
                          down="driver_hair_00",
                          left="driver_l_ear",
                          right="driver_r_ear"))
'''
# head_ctrl
pick_data.append(pickInfo(control="head_ctrl",
                          up="torso_ctrl",
                          down="head_ctrl",
                          left="head_ctrl",
                          right="head_ctrl"))
'''
#################
# hair controls #
#################
hair_length = 4
for i in range(0, hair_length):
    parent_control = ["driver_hair_0%s" % (i-1), "head_ctrl" ]
    pick_data.append(pickInfo(control="driver_hair_0%s" % i,
                      up=parent_control[i == 0],
                      down="driver_hair_0%s" % min(i+1, hair_length-1),
                      left="driver_hair_0%s" % i,
                      right="driver_hair_0%s" % i))
'''
# add the attributes
tbpw.setup_pickwalking(pick_data)
