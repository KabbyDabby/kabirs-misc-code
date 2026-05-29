stage_1 = [[20, 24], [20, 24, 26, 28, 30, 32, 36]]
stage_2 = [[15, 20], [20, 24]]
stage_3 = [[18], [52, 56]]


base_rpm = 6000


final_rpms = {}

stage_1_ratios = {}
stage_2_ratios = {}
stage_3_ratios = {}

for i in range(len(stage_1[0])):
    for j in range(len(stage_1[1])):
        ratio = stage_1[0][i] / stage_1[1][j]
        stage_1_ratios[ratio] = f"{stage_1[0][i]}:{stage_1[1][j]}"

for i in range(len(stage_2[0])):
    for j in range(len(stage_2[1])):
        ratio = stage_2[0][i] / stage_2[1][j]
        stage_2_ratios[ratio] = f"{stage_2[0][i]}:{stage_2[1][j]}"

for i in range(len(stage_3[0])):
    for j in range(len(stage_3[1])):
        ratio = stage_3[0][i] / stage_3[1][j]
        stage_3_ratios[ratio] = f"{stage_3[0][i]}:{stage_3[1][j]}"


for stage_1_ratio in stage_1_ratios:
    for stage_2_ratio in stage_2_ratios:
        for stage_3_ratio in stage_3_ratios:
            final_rpm = base_rpm
            final_rpm *= stage_1_ratio
            final_rpm *= stage_2_ratio
            final_rpm *= stage_3_ratio
            final_rpms[final_rpm] = (
                f"{stage_1_ratios[stage_1_ratio]}, {stage_2_ratios[stage_2_ratio]}, {stage_3_ratios[stage_3_ratio]}"
            )

for rpm in sorted(
    [rpm for rpm in final_rpms.keys() if rpm > 900 and rpm < 1200], reverse=True
):
    print(f"{rpm}: {final_rpms[rpm]}")
