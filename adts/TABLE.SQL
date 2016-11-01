CREATE TABLE `TESTING_INFO` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`tsi_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(64) NOT NULL COMMENT '테스트 이름',
		`discription` text NOT NULL COMMENT '테스트 목적',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`tsi_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `ENV_SETTING` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`ens_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`tsi_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`item` varchar(64) NOT NULL COMMENT '아이템',
		`value` text NOT NULL COMMENT '값',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`ens_uid`,`tsi_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `SCENARIO_GROUP` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`scg_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`scg_uid_parent` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(64) NOT NULL COMMENT '시나리오 이름',
		`discription` text DEFAULT NULL COMMENT '설명',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`scg_uid`,`scg_uid_parent`,`name`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `SCENARIO` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`sce_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`scg_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(64) NOT NULL COMMENT '시나리오 이름',
		`discription` text DEFAULT NULL COMMENT '설명',
		`param` varchar(64) DEFAULT NULL COMMENT '메소드의 파라메터',
		`param_ext` text DEFAULT NULL COMMENT '추가 파라메터',
		`classname` varchar(64) NOT NULL COMMENT '클래스 이름',
		`type` varchar(10) DEFAULT NULL COMMENT '',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`sce_uid`,`scg_uid`,`name`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `SCENARIO_LINE` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`scl_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`sce_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`index` int(11) NOT NULL COMMENT '인덱스 ',
		`method` varchar(64) NOT NULL COMMENT '실행 메소드 이름',
		`title` text DEFAULT NULL COMMENT '화면에 나오는 문자열',
		`param` varchar(64) DEFAULT NULL COMMENT '메소드의 파라메터',
		`param_ext` text DEFAULT NULL COMMENT '추가 파라메터',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`scl_uid`,`sce_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `PACKET` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`pck_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(64) NOT NULL COMMENT '패킷 이름',
		`type` varchar(64) DEFAULT NULL COMMENT '패킷 종류',
		`discription` text NOT NULL COMMENT '설명',
		`make_class` varchar(64) NOT NULL COMMENT '클래스 이름',
		`confirm_class` varchar(64) NOT NULL COMMENT '클래스 이름',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`pck_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `PACKET_DATA_UNIT` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`pdu_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`pck_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`index` int(11) NOT NULL COMMENT '단위 시나리오의 인덱스 ',
		`pdt_uid` varchar(20) NOT NULL COMMENT '',
		`def_value` varchar(10)  COMMENT '고정값',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`pdu_uid`,`pck_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `PACKET_DATA_TYPE` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`pdt_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(64) NOT NULL COMMENT '패킷 유닛 이름',
		`length` int(11) NOT NULL COMMENT '패킷 유닛의 크기',
		`variation` varchar(10)  COMMENT '가변',
		`value_encoding` varchar(10) NOT NULL COMMENT '인코딩',
		`char_range` varchar(10)  COMMENT '문자범위',
		`fixed_value` varchar(10)  COMMENT '고정값',
		`option` varchar(64) DEFAULT NULL COMMENT '메소드의 파라메터',
		`make_param` text DEFAULT NULL COMMENT '',
		`confirm_param` text DEFAULT NULL COMMENT '추가 파라메터',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`pdt_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `DATA_VALUE_TABLE` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`dvt_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`scl_uid` varchar(20) DEFAULT NULL COMMENT '',
		`pdt_uid` varchar(20) NOT NULL COMMENT '',
		`value` text DEFAULT NULL COMMENT '설명',
		`param` varchar(64) DEFAULT NULL COMMENT '메소드의 파라메터',
		`param_ext` text DEFAULT NULL COMMENT '추가 파라메터',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`dvt_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `MAIN_PROCESS` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`mpr_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`sce_uid` varchar(20) DEFAULT NULL COMMENT '',
		`index` int(11) NOT NULL COMMENT '',
		`type` varchar(10) DEFAULT NULL COMMENT '',
		`name` varchar(64) NOT NULL COMMENT '시나리오 이름',
		`discription` text DEFAULT NULL COMMENT '설명',
		`method` varchar(64) NOT NULL COMMENT '',
		`param` varchar(64) DEFAULT NULL COMMENT '메소드의 파라메터',
		`param_ext` text DEFAULT NULL COMMENT '추가 파라메터',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`mpr_uid`,`name`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `CHANNEL` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`chn_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`name` varchar(10) NOT NULL COMMENT '시나리오 이름',
		`type` varchar(10) NOT NULL COMMENT '',
		`discription` varchar(20) DEFAULT NULL COMMENT '설명',
		`param` varchar(64) DEFAULT NULL COMMENT '',
		`classname` varchar(64) DEFAULT NULL COMMENT '클래스 이름',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`chn_uid`,`name`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `TEST_RESULT` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`tsr_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`tsi_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`title` varchar(64) DEFAULT NULL COMMENT '테스트 이름',
		`data` text DEFAULT NULL COMMENT '테스트 목적',
		`result` varchar(20) DEFAULT NULL COMMENT '',
		`takentime` int(11) DEFAULT NULL COMMENT '',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`tsr_uid`,`tsi_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



CREATE TABLE `DATA_RESULT` (
		`seq` int(11) NOT NULL COMMENT '순번',
		`dtr_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`tsr_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
		`pdt_uid` varchar(20) NOT NULL COMMENT '',
		`value` text DEFAULT NULL COMMENT '',
		`etc` text DEFAULT NULL COMMENT '',
		`updt_date` datetime NOT NULL COMMENT '업데이트일자',
		`reg_date` datetime NOT NULL COMMENT '등록일자',
		`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`dtr_uid`,`tsr_uid`) 
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;



