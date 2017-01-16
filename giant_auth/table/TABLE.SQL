
CREATE TABLE `chip` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`chp_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`sn` varchar(20) DEFAULT NULL COMMENT '시리얼 넘버',
	`msk_uid` varchar(20) DEFAULT NULL COMMENT '',
	`slot_no` int(11) DEFAULT NULL COMMENT 'chip 의 slot no ',
	`updt_date` datetime NOT NULL COMMENT '업데이트 일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`chp_uid`,`sn`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
CREATE TABLE `masterkey` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`msk_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`key_value` text DEFAULT NULL COMMENT '암호키',
	`version` varchar(10) DEFAULT NULL COMMENT '마스터 키 버전',
	`updt_date` datetime NOT NULL COMMENT '업데이트 일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`msk_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
CREATE TABLE `session` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`ssn_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`chp_uid` varchar(20) DEFAULT NULL COMMENT '칩 고유 ID',
	`msk_uid` varchar(20) DEFAULT NULL COMMENT '마스터키 고유 ID',
	`latest_msk_uid` varchar(20) DEFAULT NULL COMMENT '최근 등록된 마스터 키 고유 ID',
	`challenge` varchar(64) DEFAULT NULL COMMENT '서버 CHALLEGE 값',
	`hostchallenge` varchar(40) DEFAULT NULL COMMENT '호스트 CHALLENGE 값',
	`updt_date` datetime NOT NULL COMMENT '업데이트 일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`ssn_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	