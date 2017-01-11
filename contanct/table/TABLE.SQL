
CREATE TABLE `contact` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`ctt_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`name` varchar(20) NOT NULL COMMENT '',
	`dpt_uid` varchar(20) NOT NULL COMMENT '',
	`tem_uid` varchar(20) NOT NULL COMMENT '',
	`pos_uid` varchar(20) NOT NULL COMMENT '',
	`company_phone` varchar(20) NOT NULL COMMENT '',
	`mobile` varchar(20) NOT NULL COMMENT '',
	`e-mail` varchar(64) NOT NULL COMMENT '',
	`birthday` varchar(20) DEFAULT NULL COMMENT '',
	`address` text DEFAULT NULL COMMENT '',
	`memo` text DEFAULT NULL COMMENT '',
	`updt_date` datetime NOT NULL COMMENT '업데이트일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`ctt_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
CREATE TABLE `depart` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`dpt_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`name` varchar(64) NOT NULL COMMENT '',
	`updt_date` datetime NOT NULL COMMENT '업데이트일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`dpt_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
CREATE TABLE `team` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`tem_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`name` varchar(64) NOT NULL COMMENT '',
	`updt_date` datetime NOT NULL COMMENT '업데이트일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`tem_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	
CREATE TABLE `pos` (
	`seq` int(11) NOT NULL COMMENT '순번',
	`pos_uid` varchar(20) NOT NULL COMMENT '고유 아이디',
	`name` varchar(64) NOT NULL COMMENT '',
	`updt_date` datetime NOT NULL COMMENT '업데이트일자',
	`reg_date` datetime NOT NULL COMMENT '등록일자',
	`comment` text DEFAULT NULL COMMENT '기타정보',
PRIMARY KEY (`seq`,`pos_uid`)
 ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
	