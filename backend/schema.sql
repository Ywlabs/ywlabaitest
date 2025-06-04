-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: ywlabs
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `intents`
--

DROP TABLE IF EXISTS `intents`;
CREATE TABLE `intents` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '인텐트 ID',
  `tag` varchar(50) NOT NULL COMMENT '인텐트 태그',
  `description` varchar(255) DEFAULT NULL COMMENT '인텐트 설명',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB COMMENT='의도 분류 테이블';

--
-- Dumping data for table `intents`
--

LOCK TABLES `intents` WRITE;
INSERT INTO `intents` (tag, description) VALUES 
('greeting','인사'),
('organization','조직도'),
('vacation','휴가'),
('esg','ESG 경영'),
('compliance','준법경영'),
('about','회사 소개'),
('history','회사 연혁'),
('vision','비전과 미션'),
('location','오시는 길'),
('contact','문의하기'),
('employee_info','직원 정보'),
('esg_info','ESG 정보');
UNLOCK TABLES;

--
-- Table structure for table `patterns`
--

DROP TABLE IF EXISTS `patterns`;
CREATE TABLE `patterns` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '패턴 ID',
  `pattern` text NOT NULL COMMENT '패턴 텍스트',
  `intent_tag` varchar(50) NOT NULL COMMENT '연관된 인텐트 태그',
  `pattern_type` varchar(20) NOT NULL DEFAULT 'static' COMMENT '패턴 유형 (static/dynamic)',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '활성화 여부',
  `priority` int NOT NULL DEFAULT 0 COMMENT '우선순위',
  `response_id` int DEFAULT NULL COMMENT '연결된 응답 ID',
  `description` varchar(255) DEFAULT NULL COMMENT '패턴 설명',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  PRIMARY KEY (`id`),
  KEY `intent_tag` (`intent_tag`),
  KEY `response_id` (`response_id`)
) ENGINE=InnoDB COMMENT='패턴 매칭 테이블';

--
-- Dumping data for table `patterns`
--

LOCK TABLES `patterns` WRITE;
INSERT INTO `patterns` (pattern, intent_tag, pattern_type, priority, response_id, description) VALUES 
('안녕하세요','greeting', 'static', 0, 1, '기본 인사 패턴'),
('조직도','organization', 'static', 0, 2, '조직도 조회 패턴'),
('휴가','vacation', 'static', 0, 3, '휴가 조회 패턴'),
('ESG','esg', 'static', 0, 4, 'ESG 조회 패턴'),
('준법','compliance', 'static', 0, 5, '준법 조회 패턴'),
('회사 소개','about', 'static', 20, 6, '회사 소개 명확 패턴'),
('회사 연혁','history', 'static', 0, 7, '회사 연혁 조회 패턴'),
('비전','vision', 'static', 0, 8, '비전 조회 패턴'),
('오시는 길','location', 'static', 0, 9, '오시는 길 조회 패턴'),
('문의','contact', 'static', 0, 10, '문의 조회 패턴'),
('영우랩스 {name} 정보','employee_info', 'dynamic', 10, 11, '직원 정보 조회 패턴 (회사명 포함)'),
('{name} 정보', 'employee_info', 'dynamic', 2, 11, '직원 정보 조회 패턴 (이름만)'),
('ESG 경영정보', 'esg_info', 'static', 0, 12, 'ESG 경영 정보 패턴');
UNLOCK TABLES;

--
-- Table structure for table `responses`
--

DROP TABLE IF EXISTS `responses`;
CREATE TABLE `responses` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '응답 ID',
  `intent_tag` varchar(50) NOT NULL COMMENT '연관된 인텐트 태그',
  `response` text NOT NULL COMMENT '응답 텍스트',
  `response_type` varchar(20) NOT NULL DEFAULT 'text' COMMENT '응답 데이터 유형 (text: 일반 텍스트, dynamic: 동적 텍스트 등, UI 유형은 route_code로 분기)',
  `template_variables` text DEFAULT NULL COMMENT '동적응답 변수',
  `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '활성화 여부',
  `priority` int NOT NULL DEFAULT 0 COMMENT '우선순위',
  `description` varchar(255) DEFAULT NULL COMMENT '응답 설명',
  `route_code` varchar(20) DEFAULT NULL COMMENT '연관된 라우트 코드',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  PRIMARY KEY (`id`),
  KEY `intent_tag` (`intent_tag`),
  KEY `route_code` (`route_code`)
) ENGINE=InnoDB COMMENT='응답 템플릿 테이블';

--
-- Dumping data for table `responses`
--

LOCK TABLES `responses` WRITE;
INSERT INTO `responses` (intent_tag, response, response_type, priority, description, route_code) VALUES 
('greeting', '안녕하세요! 영우랩스 AI 어시스턴트입니다. 무엇을 도와드릴까요?', 'text', 0, '기본 인사 응답', NULL),
('organization', '조직도를 확인하시겠습니까?', 'text', 0, '조직도 조회 응답', 'ORG_CHART'),
('vacation', '휴가 정보를 확인하시겠습니까?', 'text', 0, '휴가 조회 응답', 'VAC_CAL'),
('esg', 'ESG 경영 정보를 확인하시겠습니까?', 'text', 0, 'ESG 조회 응답', 'ESG_INFO'),
('compliance', '준법경영 정보를 확인하시겠습니까?', 'text', 0, '준법 조회 응답', 'CMP_INFO'),
('about', '회사 소개 페이지로 이동하시겠습니까?', 'text', 0, '회사 소개 응답', 'ABOUT'),
('history', '회사 연혁 페이지로 이동하시겠습니까?', 'text', 0, '회사 연혁 응답', 'HISTORY'),
('vision', '비전과 미션 페이지로 이동하시겠습니까?', 'text', 0, '비전과 미션 응답', 'VISION'),
('location', '오시는 길 페이지로 이동하시겠습니까?', 'text', 0, '오시는 길 응답', 'LOCATION'),
('contact', '문의하기 페이지로 이동하시겠습니까?', 'text', 0, '문의하기 응답', 'CONTACT'),
('employee_info', '{employee.name}님의 정보입니다:\n직책: {employee.position}\n부서: {employee.dept_nm}\n이메일: {employee.email}\n연락처: {employee.phone}', 'dynamic', 0, '직원 정보 동적 응답', NULL),
('esg_info', 'ESG 경영 정보를 안내해드릴까요?', 'text', 0, 'ESG 경영 정보 응답', 'ESG_INFO');
UNLOCK TABLES;

--
-- Table structure for table `vector_store`
--

DROP TABLE IF EXISTS `vector_store`;
CREATE TABLE `vector_store` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '벡터 ID',
  `pattern_id` int NOT NULL COMMENT '연관된 패턴 ID',
  `vector` json NOT NULL COMMENT '임베딩 벡터',
  `pattern_text` text NOT NULL COMMENT '패턴 텍스트',
  `response` text NOT NULL COMMENT '응답 텍스트',
  `target_url` varchar(255) DEFAULT NULL COMMENT '대상 URL',
  `button_text` varchar(100) DEFAULT NULL COMMENT '버튼 텍스트',
  `vector_status` varchar(20) DEFAULT 'pending' COMMENT '벡터 처리 상태',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  PRIMARY KEY (`id`),
  KEY `pattern_id` (`pattern_id`),
  KEY `idx_vector_status` (`vector_status`)
) ENGINE=InnoDB COMMENT='벡터 저장소 테이블';

--
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '대화 ID',
  `user_message` text NOT NULL COMMENT '사용자 메시지',
  `ai_response` text NOT NULL COMMENT 'AI 응답',
  `intent_tag` varchar(50) DEFAULT NULL COMMENT '인식된 인텐트 태그',
  `route_code` varchar(20) DEFAULT NULL COMMENT '연관된 라우트 코드',
  `response_source` varchar(20) NOT NULL DEFAULT 'db' COMMENT '응답 소스 (db/gpt/hybrid)',
  `response_time` float DEFAULT NULL COMMENT '응답 생성 소요 시간(초)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  `response_json` json DEFAULT NULL COMMENT 'AI 응답 전체 JSON',
  PRIMARY KEY (`id`),
  KEY `idx_intent_tag` (`intent_tag`),
  KEY `idx_route_code` (`route_code`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB COMMENT='채팅 히스토리 테이블';

--
-- Table structure for table `vector_update_logs`
--

DROP TABLE IF EXISTS `vector_update_logs`;
CREATE TABLE `vector_update_logs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '로그 ID',
  `pattern_id` int NOT NULL COMMENT '연관된 패턴 ID',
  `status` varchar(20) NOT NULL COMMENT '처리 상태',
  `error_message` text COMMENT '에러 메시지',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  PRIMARY KEY (`id`),
  KEY `pattern_id` (`pattern_id`)
) ENGINE=InnoDB COMMENT='벡터 업데이트 로그 테이블';

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '직원 ID',
  `name` varchar(50) NOT NULL COMMENT '이름',
  `email` varchar(100) DEFAULT NULL COMMENT '이메일',
  `phone` varchar(20) DEFAULT NULL COMMENT '연락처',
  `position` varchar(50) DEFAULT NULL COMMENT '직책',
  `dept_nm` varchar(50) DEFAULT NULL COMMENT '부서명',
  `sns` varchar(200) DEFAULT NULL COMMENT 'SNS 링크',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_name_dept` (`name`, `dept_nm`),
  KEY `idx_position_dept` (`position`, `dept_nm`)
) ENGINE=InnoDB COMMENT='직원 정보 테이블';

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
INSERT INTO `employees` (name, email, phone, position, dept_nm, sns) VALUES 
('조정현', 'amma76@ywlabs.com', '010-1234-5678', '대표이사', '경영지원', 'https://linkedin.com/in/hong'),
('유석준', 'plan@ywlabs.com', '010-2345-6789', '전략기획이사', '전략기획팀', 'https://github.com/devkim'),
('백승욱', 'bsu@ywlabs.com', '010-3456-7890', '개발이사', '기술연구소', 'https://instagram.com/marketinglee'),
('김학현', 'hyuni0242@ywlabs.com', '010-3456-7890', '기획팀장', '전략기획팀', 'https://instagram.com/marketinglee'),
('이성구', 'lsg@ywlabs.com', '010-3456-7890', '개발팀장', '기술연구소', 'https://instagram.com/marketinglee'),
('이채유', 'chaeyu@ywlabs.com', '010-3456-7890', '사우회장', '전략기획팀', 'https://instagram.com/marketinglee'),
('김정규', 'wjdrb0636@ywlabs.com', '010-3456-7890', '선임연구원', '기술연구소', 'https://instagram.com/marketinglee'),
('최동민', 'cdm0614@ywlabs.com', '010-3456-7890', '선임연구원', '기술연구소', 'https://instagram.com/marketinglee'),
('편재준', 'hil04050@ywlabs.com', '010-3456-7890', '주임연구원', '기술연구소', 'https://instagram.com/marketinglee'),
('박주희', 'juhee99@ywlabs.com', '010-3456-7890', '주임연구원', '기술연구소', 'https://instagram.com/marketinglee');
UNLOCK TABLES;

--
-- Table structure for table `routes`
--

DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes` (
  `route_code` varchar(20) NOT NULL COMMENT '라우트 코드',
  `route_name` varchar(100) NOT NULL COMMENT '라우트 이름',
  `route_path` varchar(200) NOT NULL COMMENT '라우트 경로',
  `route_type` varchar(20) NOT NULL COMMENT '라우트 유형 (widget: 위젯, link: 링크, button: 버튼 등 UI 유형)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
  PRIMARY KEY (`route_code`)
) ENGINE=InnoDB COMMENT='라우트 정보 테이블';

--
-- Dumping data for table `routes`
--

LOCK TABLES `routes` WRITE;
INSERT INTO `routes` (route_code, route_name, route_path, route_type) VALUES 
('ORG_CHART', '조직도', '/organization', 'widget'),
('VAC_CAL', '휴가 캘린더', '/vacation', 'widget'),
('ESG_INFO', 'ESG 경영', '/esg', 'widget'),
('CMP_INFO', '준법경영', '/compliance', 'widget'),
('ABOUT', '회사 소개', '/about', 'link'),
('HISTORY', '회사 연혁', '/history', 'link'),
('VISION', '비전과 미션', '/vision', 'link'),
('LOCATION', '오시는 길', '/location', 'link'),
('CONTACT', '문의하기', '/contact', 'link');
UNLOCK TABLES;

--
-- Table structure for table `search_logs`
--

DROP TABLE IF EXISTS `search_logs`;
CREATE TABLE `search_logs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '로그 ID',
  `query` text NOT NULL COMMENT '검색 쿼리',
  `results` text NOT NULL COMMENT '검색 결과',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='검색 로그 테이블';