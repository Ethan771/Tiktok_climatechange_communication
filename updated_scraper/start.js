require('./env')
require('./a_bogus')



function get_a_bogus(params) {
    u = [
        0,
        1,
        0,
        params,
        "",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    ]
    var r = window._U._v;
    return (0,
        window._U._u)(r[0], u, r[1], r[2], this)
}
// param = "device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAAH2lnQkBKMmSgBKVmAF3-uy5c4lxHTUou810jesbDogCBHw3PJObaedZQlsNQvyYP&max_cursor={page_number}&locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token=&cut_version=1&count=18&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=114.0.0.0&browser_online=true&engine_name=Blink&engine_version=114.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7274486964056081972&msToken=n3BVahBaE3Xl4MND7Er13RALLnjixCerHp6KlKgBi1CxYx52hp4SBybAguXl7ShlOSBFXhRs_5UNK_v-rOkzm3rHJATG0W4OcDDzXCo-bewrTEGeUzeyqUFFG14l"
// console.log(get_a_bogus())