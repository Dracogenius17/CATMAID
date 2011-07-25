<?php

/**
 * session.class.php
 *
 * @author Stephan Saalfeld <saalfeld@phenomene.de>
 * @copyright Copyright (c) 2006, Stephan Saalfeld
 * @version 0.1 TrakEM2
 *
 */
/**
 */
include_once( 'db.pg.class.php' );
include_once( 'auth_ldap.inc.php' );

/**
 * factory method to get the single instance of the object
 *
 * @return Session singleton instance
 */
function &getSession()
{
	static $session;
	if ( !isset( $session ) )
	{
		$session = new Session();
	}
	return $session;
}

/**
 * Session
 *
 * provides Methods to instanciate a session and check permissions
 *
 * @package pRED
 */
class Session
{
	/**
	 * @var DB $db
	 *
	 * @access private
	 */
	var $db;

	/**
	 * @var string $session_key
	 *
	 * @access private
	 */
	var $session_key = '7gtmcy8g03457xg3hmuxdgregtyu45ty57ycturemuzm934etmvo56';

	/**
	 * @access private
	 */
	function Session() 
	{
		session_start();
		$this->db =& getDB();
	}
	
	/**
	 * create a session
	 *
	 * @param int $name user account (DB: "user"."name")
	 */
	function create( $id )
	{
		$_SESSION[ 'id' ] = $id;
		$_SESSION[ 'key' ] = $this->session_key;
		return;
	}
	
	/**
     * checks db if a user supplied correct password and if the user account is valid
	 *
	 * @param string $_user user account (DB: "user"."name")
	 * @param string $_pwd user password (DB: "user"."pwd")
	 *
	 * @return false|id
     */
	function isUserValid( $name, $pwd )
	{
		global $fallbackToLDAP;
		if ( $pwd == '' ) return FALSE;
		$v = $this->db->getResult(
			'SELECT	*
			
				FROM	"user"
				
				WHERE	"name" = \''.pg_escape_string( $name ).'\' AND
						"pwd" = MD5( \''.pg_escape_string( $pwd ).'\' ) AND
						NOT ldap' );
		if ( $v && isset( $v[ 0 ] ) && isset( $v[ 0 ][ 'id' ] ) )
			return $v[ 0 ][ 'id' ];
		else {
			error_log("fallbackToLDAP is: $fallbackToLDAP");
			if( isset($fallbackToLDAP) && $fallbackToLDAP ) {
				$result = authValidateUser($name, $pwd);
				error_log("got back from ldap: ".print_r($result, TRUE));
				if ($result == 0) {
					return false;
				}
				error_log("authentication with LDAP was successful!");
				error_log("result is: ".print_r($result,TRUE));
				try {
					$v = $this->db->getResult('INSERT INTO "user" (name, pwd, ldap) VALUES (\''.pg_escape_string( $name ).'\', \'\', True) RETURNING id');
					if ( $v && isset( $v[ 0 ] ) && isset( $v[ 0 ][ 'id' ] ) )
						$new_ldap_user_id = $v[ 0 ][ 'id' ];
					else
						return false;

					$fullName = authLdapGetFullUsername($name);
					$this->db->getResult('UPDATE "user" SET longname = \''.pg_escape_string( $fullName ).'\' WHERE id = '.$new_ldap_user_id);

					return $new_ldap_user_id;
				} catch (Exception $e) {
					// The INSERT failed, which must be because the
					// UNIQUE constraint on the name column failed.
					// This means one of two things - either there's
					// an existing non-LDAP account associated with
					// that name, or this isn't the first time someone
					// has logged in.  Distinguish between these
					// cases:
					$v = $this->db->getResult('SELECT id, ldap FROM "user" WHERE name = \''.pg_escape_string( $name ).'\'');
					if ( $v && isset( $v[0] ) && isset( $v[0]['id'] ) && isset( $v[0]['ldap'] ) ) {
						if( $v[0]['ldap'] ) {
							return $v[0]['id'];
						} else {
							return false;
						}
					} else {
						return false;
					}
				}
			} else {
				return false;
			}
		}
	}

	/**
	 * deletes current Session
	 *
	 * @return boolean true
	 */
	function deleteSession()
	{
		if ( isset( $_COOKIE[ session_name() ] ) )
		{
    		setcookie( session_name(), '', time() - 42000, '/' );
		}
		@session_destroy();
		return true;
	}

	/**
	 * open a session request, check permission
	 * if not permitted, wait for 2sec return an error and exit
	 *
	 * @return boolean true
	 */
	function open()
	{
		if ( $this->isSessionValid() )
			return true;
		else
		{
			sleep( 2 );
			$this->deleteSession();
			echo 'Invalid session.';
    		exit;
		}
	}

	/**
	 * get the id of the user holding the current session
	 *
	 * @return int $_SESSION[ 'id' ] that corresponds to (DB: "user"."id")
	 */
	function getId()
	{
		return $_SESSION[ 'id' ];
	}
	
	/**
	 * get the user data of the user who owns the current session
	 *
	 * @return array|false
	 */
	function getData()
	{
		$d = false;
		if ( $_SESSION[ 'id' ] )
			$d = $this->db->getResult(
				'SELECT	"id",
						"name",
						"longname"
				
					FROM	"user"
					
					WHERE	"id" = '.$_SESSION[ 'id' ] );
		if ( $d && isset( $d[ 0 ] ) ) return $d[ 0 ];
		else return false;
	}
	

	/**
	 * checks if the current session is still valid
	 *
	 * @return boolean
	 *
	 * @access private
	 */
	function isSessionValid()
	{
		return isset( $_SESSION[ 'id' ] ) && isset( $_SESSION[ 'key' ] ) && $_SESSION[ 'key' ] == $this->session_key;
	}
}

?>
