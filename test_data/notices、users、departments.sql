
INSERT INTO `notices`(`id`, `title`, `content`, `create_time`, `updateTime`) VALUES (1, '发热门诊筛查', '  若您出现发热、呼吸道症状（咳嗽、打喷嚏、流鼻涕）、胸闷等症状，请立即前往“发热门诊”筛查。挂号、开检查单、新冠病毒检测等全部在发热门诊完成。', '2022-05-19 20:35:54.785993', NULL);
INSERT INTO `notices`(`id`, `title`, `content`, `create_time`, `updateTime`) VALUES (2, '五一放假安排', '五一放假安排还是按原来说的那样做！', '2022-05-19 20:49:06.340424', '2022-05-20 00:16:46.000000');

INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (1, 'admin', 'admin', '2020-05-19 15:53:00.000000', NULL, 0);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (2, 'zhangsan', 'zhangsan', '2022-05-19 18:53:59.000000', NULL, 1);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (3, 'lisi', 'lisi', '2022-05-19 18:54:16.000000', NULL, 1);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (4, 'wangwu', 'wangwu', '2022-05-19 18:54:37.000000', NULL, 1);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (5, 'zhaoliu', 'zhaoliu', '2022-05-19 18:55:06.000000', NULL, 1);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (6, 'sumei', 'sumei', '2022-05-19 18:56:12.000000', NULL, 2);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (7, 'ssl', 'ssl', '2022-05-19 18:56:30.000000', NULL, 2);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (8, 'kiri', 'kiri', '2022-05-19 18:56:59.000000', NULL, 2);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (9, 'tengmao', 'tengmao', '2022-05-19 18:57:21.000000', NULL, 2);
INSERT INTO `users`(`id`, `user_name`, `pass_word`, `create_time`, `update_time`, `type`) VALUES (10, 'kamisama', 'kamisama', '2022-05-19 18:57:41.000000', NULL, 0);


INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (1, '101', '内科', '内科门诊，包括呼吸内科、消化内科、神经内科、心血管内科、血液内科、肾病学、内分泌、免疫学、变态反应、老年病、内科其他等门诊', NULL, 1, '2022-05-19 18:50:34.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (2, '102', '外科', '包括普通外科、肝脏移植、胰腺移植、小肠移植、神经外科、骨科、泌尿外科、肾病移植、胸外科、肺脏移植、心脏移植、整形外科、烧伤外科等外科门诊', NULL, 1, '2022-05-19 18:52:20.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (3, '103', '妇产科', '妇产科包括妇科、产科、计划生育、优生学、生殖健康与不孕症等门诊', NULL, 1, '2022-05-19 18:53:24.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (4, '104', '急诊科', '急诊科门诊', NULL, 1, '2022-05-19 19:16:37.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (5, '105', '检验科', '检验科', NULL, 1, '2022-05-19 19:16:37.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (6, '106', '麻醉科', '麻醉科门诊', NULL, 1, '2022-05-19 19:20:36.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (7, '107', '儿科', '儿科门诊包括新生儿门诊、小儿传染病门诊、小儿消化门诊、小儿呼吸门诊、小儿心脏病门诊、小儿肾病门诊、小儿神经病学门诊、小儿内分泌门诊、小儿遗传病门诊、小儿免疫门诊、儿科其他门诊', NULL, 1, '2022-05-19 19:02:50.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (8, '108', '眼科', '眼科门诊', NULL, 1, '2022-05-19 19:05:57.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (9, '109', '耳鼻咽喉科', '耳鼻咽喉科门诊包括耳科门诊、鼻科门诊、咽喉门诊、耳鼻咽喉科其他门诊', NULL, 1, '2022-05-19 19:07:01.000000');
INSERT INTO `departments`(`id`, `did`, `name`, `describe`, `update_time`, `status`, `create_time`) VALUES (10, '110', '口腔科', '口腔科门诊包括牙体牙髓病门诊、牙周病门诊、口腔粘膜病门诊、儿童口腔门诊、口腔颌面外科门诊、口腔修复门诊、口腔正畸门诊、口腔种植门诊、预防口腔门诊、口腔科其他门诊', NULL, 1, '2022-05-19 19:08:52.000000');