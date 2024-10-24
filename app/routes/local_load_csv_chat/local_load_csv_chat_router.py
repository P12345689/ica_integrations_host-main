# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, adapted by Matt Colman for local-load
Description: Local Load Chat Integration Router

This module provides a FastAPI router for chatting with CSV data using pandas and an LLM.
The CSV content is stored within the router and loaded based on specification from requestor.

Security Measures and Implementing Functions:
1. Input validation and sanitization:
   - User queries are sanitized to remove potentially harmful keywords and characters (sanitize_user_input).
   - Dataframe size (rows and columns) is restricted to prevent memory exhaustion (validate_dataframe).

2. Safe code execution:
   - The generated Python code is sanitized to prevent the use of unsafe functions and modules (sanitize_code).
   - A blocklist is used to disallow the use of potentially dangerous operations (sanitize_code).
   - An allowlist is used to restrict the available functions and modules to a safe subset (sanitize_code).
   - The code is executed in a separate function with a restricted global namespace (execute_code_with_timeout).
   - Execution time is limited to prevent infinite loops or long-running operations (execute_code_with_timeout).

3. Error handling and logging:
   - Detailed error messages are logged for debugging purposes (throughout the module, using the 'log' object).
   - Error messages returned to the user are kept generic to avoid leaking sensitive information (chat_with_csv, get_csv_info).
   - Exceptions are caught and handled gracefully to prevent unhandled errors (chat_with_csv, get_csv_info).

4. Asynchronous processing:
   - The module uses asynchronous functions to handle time-consuming operations like loading dataframes and making API calls (load_dataframe, process_csv_chat, execute_code_with_timeout).

5. Retry mechanism:
   - The module includes a retry mechanism to handle temporary failures when parsing the LLM response (chat_with_csv).

6. Secure dataframe loading:
   - A separate function is used to safely load and validate dataframes (safe_load_dataframe).

7. Data handling:
   - Sensitive data in the CSV files is not persisted beyond the scope of a single request (all data is handled in-memory in chat_with_csv and get_csv_info).
   - Data is kept in memory and not written to disk when possible (using StringIO and BytesIO in load_dataframe).

Key Functions:
- add_custom_routes(app: FastAPI): Adds the CSV chat routes to the FastAPI application.
- chat_with_csv(...): Handles the main chat functionality, orchestrating the entire process.
- get_csv_info(...): Provides information about the uploaded CSV file.
- load_dataframe(...): Loads the CSV data from various sources with initial validations.
- safe_load_dataframe(...): Combines loading and comprehensive validation of dataframes.
- validate_dataframe(df: pd.DataFrame): Performs security checks on the loaded dataframe.
- sanitize_user_input(input_str: str): Sanitizes user input to prevent injection attacks.
- sanitize_code(code: str): Sanitizes generated Python code to ensure safe execution.
- execute_code_with_timeout(...): Executes sanitized code with a timeout for safety.
- process_csv_chat(...): Processes the chat query using the LLM.

Usage:
    This module is intended to run on on ica_container_host, as an integration.
    No other integrations should run on the same container.

Deployment Recommendations:
1. Secure container deployment:
   - Run this module separately in a Red Hat Universal Base Image container on ica_container_host.
   - Configure the filesystem as read-only, except for a designated directory for temporary file uploads.

2. Monitoring and alerting:
   - Implement comprehensive logging and monitoring.
   - Set up alerts for abnormal behavior (high error rates, unusual resource usage).
   - Setup monitoring for container escape
   - Restrict the container's Syscalls with seccomp
"""

import asyncio
import json
import logging
import os
import re
import textwrap
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO, StringIO
from typing import List, Optional
from uuid import uuid4

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, HttpUrl

def load_csv_content(csvType: str):
    csv_content = None
    if csvType == "asvs":
        csv_content = '''chapter_id,chapter_name,section_id,section_name,req_id,req_description,level1,level2,level3,cwe,nist
V1,,V1.1,Secure Software Development Lifecycle,V1.1.1,Verify the use of a secure software development lifecycle that addresses security in all stages of development. ([C1](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.2,"Verify the use of threat modeling for every design change or sprint planning to identify threats, plan for countermeasures, facilitate appropriate risk responses, and guide security testing.",,✓,✓,1053,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.3,"Verify that all user stories and features contain functional security constraints, such as ""As a user, I should be able to view and edit my profile. I should not be able to view or edit anyone else's profile""",,✓,✓,1110,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.4,"Verify documentation and justification of all the application's trust boundaries, components, and significant data flows.",,✓,✓,1059,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.5,Verify definition and security analysis of the application's high-level architecture and all connected remote services. ([C1](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,1059,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.6,"Verify implementation of centralized, simple (economy of design), vetted, secure, and reusable security controls to avoid duplicate, missing, ineffective, or insecure controls. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,637,
V1,,V1.1,Secure Software Development Lifecycle,V1.1.7,"Verify availability of a secure coding checklist, security requirements, guideline, or policy to all developers and testers.",,✓,✓,637,
V1,,V1.2,Authentication Architecture,V1.2.1,"Verify the use of unique or special low-privilege operating system accounts for all application components, services, and servers. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,250,
V1,,V1.2,Authentication Architecture,V1.2.2,"Verify that communications between application components, including APIs, middleware and data layers, are authenticated. Components should have the least necessary privileges needed. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,306,
V1,,V1.2,Authentication Architecture,V1.2.3,"Verify that the application uses a single vetted authentication mechanism that is known to be secure, can be extended to include strong authentication, and has sufficient logging and monitoring to detect account abuse or breaches.",,✓,✓,306,
V1,,V1.2,Authentication Architecture,V1.2.4,"Verify that all authentication pathways and identity management APIs implement consistent authentication security control strength, such that there are no weaker alternatives per the risk of the application.",,✓,✓,306,
V1,,V1.4,Access Control Architecture,V1.4.1,"Verify that trusted enforcement points, such as access control gateways, servers, and serverless functions, enforce access controls. Never enforce access controls on the client.",,✓,✓,602,
V1,,V1.4,Access Control Architecture,V1.4.2,"[DELETED, NOT ACTIONABLE]",,,,,
V1,,V1.4,Access Control Architecture,V1.4.3,"[DELETED, DUPLICATE OF 4.1.3]",,,,,
V1,,V1.4,Access Control Architecture,V1.4.4,Verify the application uses a single and well-vetted access control mechanism for accessing protected data and resources. All requests must pass through this single mechanism to avoid copy and paste or insecure alternative paths. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,284,
V1,,V1.4,Access Control Architecture,V1.4.5,Verify that attribute or feature-based access control is used whereby the code checks the user's authorization for a feature/data item rather than just their role. Permissions should still be allocated using roles. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,275,
V1,,V1.5,Input and Output Architecture,V1.5.1,"Verify that input and output requirements clearly define how to handle and process data based on type, content, and applicable laws, regulations, and other policy compliance.",,✓,✓,1029,
V1,,V1.5,Input and Output Architecture,V1.5.2,"Verify that serialization is not used when communicating with untrusted clients. If this is not possible, ensure that adequate integrity controls (and possibly encryption if sensitive data is sent) are enforced to prevent deserialization attacks including object injection.",,✓,✓,502,
V1,,V1.5,Input and Output Architecture,V1.5.3,Verify that input validation is enforced on a trusted service layer. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,602,
V1,,V1.5,Input and Output Architecture,V1.5.4,Verify that output encoding occurs close to or by the interpreter for which it is intended. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,116,
V1,,V1.6,Cryptographic Architecture,V1.6.1,Verify that there is an explicit policy for management of cryptographic keys and that a cryptographic key lifecycle follows a key management standard such as NIST SP 800-57.,,✓,✓,320,
V1,,V1.6,Cryptographic Architecture,V1.6.2,Verify that consumers of cryptographic services protect key material and other secrets by using key vaults or API based alternatives.,,✓,✓,320,
V1,,V1.6,Cryptographic Architecture,V1.6.3,Verify that all keys and passwords are replaceable and are part of a well-defined process to re-encrypt sensitive data.,,✓,✓,320,
V1,,V1.6,Cryptographic Architecture,V1.6.4,"Verify that the architecture treats client-side secrets--such as symmetric keys, passwords, or API tokens--as insecure and never uses them to protect or access sensitive data.",,✓,✓,320,
V1,,V1.7,"Errors, Logging and Auditing Architecture",V1.7.1,Verify that a common logging format and approach is used across the system. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,1009,
V1,,V1.7,"Errors, Logging and Auditing Architecture",V1.7.2,"Verify that logs are securely transmitted to a preferably remote system for analysis, detection, alerting, and escalation. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,,
V1,,V1.8,Data Protection and Privacy Architecture,V1.8.1,Verify that all sensitive data is identified and classified into protection levels.,,✓,✓,,
V1,,V1.8,Data Protection and Privacy Architecture,V1.8.2,"Verify that all protection levels have an associated set of protection requirements, such as encryption requirements, integrity requirements, retention, privacy and other confidentiality requirements, and that these are applied in the architecture.",,✓,✓,,
V1,,V1.9,Communications Architecture,V1.9.1,"Verify the application encrypts communications between components, particularly when these components are in different containers, systems, sites, or cloud providers. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,319,
V1,,V1.9,Communications Architecture,V1.9.2,"Verify that application components verify the authenticity of each side in a communication link to prevent person-in-the-middle attacks. For example, application components should validate TLS certificates and chains.",,✓,✓,295,
V1,,V1.10,Malicious Software Architecture,V1.10.1,"Verify that a source code control system is in use, with procedures to ensure that check-ins are accompanied by issues or change tickets. The source code control system should have access control and identifiable users to allow traceability of any changes.",,✓,✓,284,
V1,,V1.11,Business Logic Architecture,V1.11.1,Verify the definition and documentation of all application components in terms of the business or security functions they provide.,,✓,✓,1059,
V1,,V1.11,Business Logic Architecture,V1.11.2,"Verify that all high-value business logic flows, including authentication, session management and access control, do not share unsynchronized state.",,✓,✓,362,
V1,,V1.11,Business Logic Architecture,V1.11.3,"Verify that all high-value business logic flows, including authentication, session management and access control are thread safe and resistant to time-of-check and time-of-use race conditions.",,,✓,367,
V1,,V1.12,Secure File Upload Architecture,V1.12.1,"[DELETED, DUPLICATE OF 12.4.1]",,,,,
V1,,V1.12,Secure File Upload Architecture,V1.12.2,"Verify that user-uploaded files - if required to be displayed or downloaded from the application - are served by either octet stream downloads, or from an unrelated domain, such as a cloud file storage bucket. Implement a suitable Content Security Policy (CSP) to reduce the risk from XSS vectors or other attacks from the uploaded file.",,✓,✓,646,
V1,,V1.14,Configuration Architecture,V1.14.1,"Verify the segregation of components of differing trust levels through well-defined security controls, firewall rules, API gateways, reverse proxies, cloud-based security groups, or similar mechanisms.",,✓,✓,923,
V1,,V1.14,Configuration Architecture,V1.14.2,"Verify that binary signatures, trusted connections, and verified endpoints are used to deploy binaries to remote devices.",,✓,✓,494,
V1,,V1.14,Configuration Architecture,V1.14.3,Verify that the build pipeline warns of out-of-date or insecure components and takes appropriate actions.,,✓,✓,1104,
V1,,V1.14,Configuration Architecture,V1.14.4,"Verify that the build pipeline contains a build step to automatically build and verify the secure deployment of the application, particularly if the application infrastructure is software defined, such as cloud environment build scripts.",,✓,✓,,
V1,,V1.14,Configuration Architecture,V1.14.5,"Verify that application deployments adequately sandbox, containerize and/or isolate at the network level to delay and deter attackers from attacking other applications, especially when they are performing sensitive or dangerous actions such as deserialization. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,265,
V1,,V1.14,Configuration Architecture,V1.14.6,"Verify the application does not use unsupported, insecure, or deprecated client-side technologies such as NSAPI plugins, Flash, Shockwave, ActiveX, Silverlight, NACL, or client-side Java applets.",,✓,✓,477,
V2,,V2.1,Password Security,V2.1.1,Verify that user set passwords are at least 12 characters in length (after multiple spaces are combined). ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.2,"Verify that passwords of at least 64 characters are permitted, and that passwords of more than 128 characters are denied. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.3,"Verify that password truncation is not performed. However, consecutive multiple spaces may be replaced by a single space. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.4,"Verify that any printable Unicode character, including language neutral characters such as spaces and Emojis are permitted in passwords.",✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.5,Verify users can change their password.,✓,✓,✓,620,5.1.1.2
V2,,V2.1,Password Security,V2.1.6,Verify that password change functionality requires the user's current and new password.,✓,✓,✓,620,5.1.1.2
V2,,V2.1,Password Security,V2.1.7,"Verify that passwords submitted during account registration, login, and password change are checked against a set of breached passwords either locally (such as the top 1,000 or 10,000 most common passwords which match the system's password policy) or using an external API. If using an API a zero knowledge proof or other mechanism should be used to ensure that the plain text password is not sent or used in verifying the breach status of the password. If the password is breached, the application must require the user to set a new non-breached password. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.8,Verify that a password strength meter is provided to help users set a stronger password.,✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.9,Verify that there are no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.10,Verify that there are no periodic credential rotation or password history requirements.,✓,✓,✓,263,5.1.1.2
V2,,V2.1,Password Security,V2.1.11,"Verify that ""paste"" functionality, browser password helpers, and external password managers are permitted.",✓,✓,✓,521,5.1.1.2
V2,,V2.1,Password Security,V2.1.12,"Verify that the user can choose to either temporarily view the entire masked password, or temporarily view the last typed character of the password on platforms that do not have this as built-in functionality.",✓,✓,✓,521,5.1.1.2
V2,,V2.2,General Authenticator Security,V2.2.1,"Verify that anti-automation controls are effective at mitigating breached credential testing, brute force, and account lockout attacks. Such controls include blocking the most common breached passwords, soft lockouts, rate limiting, CAPTCHA, ever increasing delays between attempts, IP address restrictions, or risk-based restrictions such as location, first login on a device, recent attempts to unlock the account, or similar. Verify that no more than 100 failed attempts per hour is possible on a single account.",✓,✓,✓,307,5.2.2 / 5.1.1.2 / 5.1.4.2 / 5.1.5.2
V2,,V2.2,General Authenticator Security,V2.2.2,"Verify that the use of weak authenticators (such as SMS and email) is limited to secondary verification and transaction approval and not as a replacement for more secure authentication methods. Verify that stronger methods are offered before weak methods, users are aware of the risks, or that proper measures are in place to limit the risks of account compromise.",✓,✓,✓,304,5.2.10
V2,,V2.2,General Authenticator Security,V2.2.3,"Verify that secure notifications are sent to users after updates to authentication details, such as credential resets, email or address changes, logging in from unknown or risky locations. The use of push notifications - rather than SMS or email - is preferred, but in the absence of push notifications, SMS or email is acceptable as long as no sensitive information is disclosed in the notification.",✓,✓,✓,620,
V2,,V2.2,General Authenticator Security,V2.2.4,"Verify impersonation resistance against phishing, such as the use of multi-factor authentication, cryptographic devices with intent (such as connected keys with a push to authenticate), or at higher AAL levels, client-side certificates.",,,✓,308,5.2.5
V2,,V2.2,General Authenticator Security,V2.2.5,"Verify that where a Credential Service Provider (CSP) and the application verifying authentication are separated, mutually authenticated TLS is in place between the two endpoints.",,,✓,319,5.2.6
V2,,V2.2,General Authenticator Security,V2.2.6,"Verify replay resistance through the mandated use of One-time Passwords (OTP) devices, cryptographic authenticators, or lookup codes.",,,✓,308,5.2.8
V2,,V2.2,General Authenticator Security,V2.2.7,Verify intent to authenticate by requiring the entry of an OTP token or user-initiated action such as a button press on a FIDO hardware key.,,,✓,308,5.2.9
V2,,V2.3,Authenticator Lifecycle,V2.3.1,"Verify system generated initial passwords or activation codes SHOULD be securely randomly generated, SHOULD be at least 6 characters long, and MAY contain letters and numbers, and expire after a short period of time. These initial secrets must not be permitted to become the long term password.",✓,✓,✓,330,5.1.1.2 / A.3
V2,,V2.3,Authenticator Lifecycle,V2.3.2,"Verify that enrollment and use of user-provided authentication devices are supported, such as a U2F or FIDO tokens.",,✓,✓,308,6.1.3
V2,,V2.3,Authenticator Lifecycle,V2.3.3,Verify that renewal instructions are sent with sufficient time to renew time bound authenticators.,,✓,✓,287,6.1.4
V2,,V2.4,Credential Storage,V2.4.1,"Verify that passwords are stored in a form that is resistant to offline attacks. Passwords SHALL be salted and hashed using an approved one-way key derivation or password hashing function. Key derivation and password hashing functions take a password, a salt, and a cost factor as inputs when generating a password hash. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,916,5.1.1.2
V2,,V2.4,Credential Storage,V2.4.2,"Verify that the salt is at least 32 bits in length and be chosen arbitrarily to minimize salt value collisions among stored hashes. For each credential, a unique salt value and the resulting hash SHALL be stored. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,916,5.1.1.2
V2,,V2.4,Credential Storage,V2.4.3,"Verify that if PBKDF2 is used, the iteration count SHOULD be as large as verification server performance will allow, typically at least 100,000 iterations. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,916,5.1.1.2
V2,,V2.4,Credential Storage,V2.4.4,"Verify that if bcrypt is used, the work factor SHOULD be as large as verification server performance will allow, with a minimum of 10. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,916,5.1.1.2
V2,,V2.4,Credential Storage,V2.4.5,"Verify that an additional iteration of a key derivation function is performed, using a salt value that is secret and known only to the verifier. Generate the salt value using an approved random bit generator [SP 800-90Ar1] and provide at least the minimum security strength specified in the latest revision of SP 800-131A. The secret salt value SHALL be stored separately from the hashed passwords (e.g., in a specialized device like a hardware security module).",,✓,✓,916,5.1.1.2
V2,,V2.5,Credential Recovery,V2.5.1,Verify that a system generated initial activation or recovery secret is not sent in clear text to the user. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,640,5.1.1.2
V2,,V2.5,Credential Recovery,V2.5.2,"Verify password hints or knowledge-based authentication (so-called ""secret questions"") are not present.",✓,✓,✓,640,5.1.1.2
V2,,V2.5,Credential Recovery,V2.5.3,Verify password credential recovery does not reveal the current password in any way. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,640,5.1.1.2
V2,,V2.5,Credential Recovery,V2.5.4,"Verify shared or default accounts are not present (e.g. ""root"", ""admin"", or ""sa"").",✓,✓,✓,16,5.1.1.2 / A.3
V2,,V2.5,Credential Recovery,V2.5.5,"Verify that if an authentication factor is changed or replaced, that the user is notified of this event.",✓,✓,✓,304,6.1.2.3
V2,,V2.5,Credential Recovery,V2.5.6,"Verify forgotten password, and other recovery paths use a secure recovery mechanism, such as time-based OTP (TOTP) or other soft token, mobile push, or another offline recovery mechanism. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,640,5.1.1.2
V2,,V2.5,Credential Recovery,V2.5.7,"Verify that if OTP or multi-factor authentication factors are lost, that evidence of identity proofing is performed at the same level as during enrollment.",,✓,✓,308,6.1.2.3
V2,,V2.6,Look-up Secret Verifier,V2.6.1,Verify that lookup secrets can be used only once.,,✓,✓,308,5.1.2.2
V2,,V2.6,Look-up Secret Verifier,V2.6.2,"Verify that lookup secrets have sufficient randomness (112 bits of entropy), or if less than 112 bits of entropy, salted with a unique and random 32-bit salt and hashed with an approved one-way hash.",,✓,✓,330,5.1.2.2
V2,,V2.6,Look-up Secret Verifier,V2.6.3,"Verify that lookup secrets are resistant to offline attacks, such as predictable values.",,✓,✓,310,5.1.2.2
V2,,V2.7,Out of Band Verifier,V2.7.1,"Verify that clear text out of band (NIST ""restricted"") authenticators, such as SMS or PSTN, are not offered by default, and stronger alternatives such as push notifications are offered first.",✓,✓,✓,287,5.1.3.2
V2,,V2.7,Out of Band Verifier,V2.7.2,"Verify that the out of band verifier expires out of band authentication requests, codes, or tokens after 10 minutes.",✓,✓,✓,287,5.1.3.2
V2,,V2.7,Out of Band Verifier,V2.7.3,"Verify that the out of band verifier authentication requests, codes, or tokens are only usable once, and only for the original authentication request.",✓,✓,✓,287,5.1.3.2
V2,,V2.7,Out of Band Verifier,V2.7.4,Verify that the out of band authenticator and verifier communicates over a secure independent channel.,✓,✓,✓,523,5.1.3.2
V2,,V2.7,Out of Band Verifier,V2.7.5,Verify that the out of band verifier retains only a hashed version of the authentication code.,,✓,✓,256,5.1.3.2
V2,,V2.7,Out of Band Verifier,V2.7.6,"Verify that the initial authentication code is generated by a secure random number generator, containing at least 20 bits of entropy (typically a six digital random number is sufficient).",,✓,✓,310,5.1.3.2
V2,,V2.8,One Time Verifier,V2.8.1,Verify that time-based OTPs have a defined lifetime before expiring.,✓,✓,✓,613,5.1.4.2 / 5.1.5.2
V2,,V2.8,One Time Verifier,V2.8.2,"Verify that symmetric keys used to verify submitted OTPs are highly protected, such as by using a hardware security module or secure operating system based key storage.",,✓,✓,320,5.1.4.2 / 5.1.5.2
V2,,V2.8,One Time Verifier,V2.8.3,"Verify that approved cryptographic algorithms are used in the generation, seeding, and verification of OTPs.",,✓,✓,326,5.1.4.2 / 5.1.5.2
V2,,V2.8,One Time Verifier,V2.8.4,Verify that time-based OTP can be used only once within the validity period.,,✓,✓,287,5.1.4.2 / 5.1.5.2
V2,,V2.8,One Time Verifier,V2.8.5,"Verify that if a time-based multi-factor OTP token is re-used during the validity period, it is logged and rejected with secure notifications being sent to the holder of the device.",,✓,✓,287,5.1.5.2
V2,,V2.8,One Time Verifier,V2.8.6,"Verify physical single-factor OTP generator can be revoked in case of theft or other loss. Ensure that revocation is immediately effective across logged in sessions, regardless of location.",,✓,✓,613,5.2.1
V2,,V2.8,One Time Verifier,V2.8.7,Verify that biometric authenticators are limited to use only as secondary factors in conjunction with either something you have and something you know.,,o,✓,308,5.2.3
V2,,V2.9,Cryptographic Verifier,V2.9.1,"Verify that cryptographic keys used in verification are stored securely and protected against disclosure, such as using a Trusted Platform Module (TPM) or Hardware Security Module (HSM), or an OS service that can use this secure storage.",,✓,✓,320,5.1.7.2
V2,,V2.9,Cryptographic Verifier,V2.9.2,"Verify that the challenge nonce is at least 64 bits in length, and statistically unique or unique over the lifetime of the cryptographic device.",,✓,✓,330,5.1.7.2
V2,,V2.9,Cryptographic Verifier,V2.9.3,"Verify that approved cryptographic algorithms are used in the generation, seeding, and verification.",,✓,✓,327,5.1.7.2
V2,,V2.10,Service Authentication,V2.10.1,"Verify that intra-service secrets do not rely on unchanging credentials such as passwords, API keys or shared accounts with privileged access.",,OS assisted,HSM,287,5.1.1.1
V2,,V2.10,Service Authentication,V2.10.2,"Verify that if passwords are required for service authentication, the service account used is not a default credential. (e.g. root/root or admin/admin are default in some services during installation).",,OS assisted,HSM,255,5.1.1.1
V2,,V2.10,Service Authentication,V2.10.3,"Verify that passwords are stored with sufficient protection to prevent offline recovery attacks, including local system access.",,OS assisted,HSM,522,5.1.1.1
V2,,V2.10,Service Authentication,V2.10.4,"Verify passwords, integrations with databases and third-party systems, seeds and internal secrets, and API keys are managed securely and not included in the source code or stored within source code repositories. Such storage SHOULD resist offline attacks. The use of a secure software key store (L1), hardware TPM, or an HSM (L3) is recommended for password storage.",,OS assisted,HSM,798,
V3,,V3.1,Fundamental Session Management Security,V3.1.1,Verify the application never reveals session tokens in URL parameters.,✓,✓,✓,598,
V3,,V3.2,Session Binding,V3.2.1,Verify the application generates a new session token on user authentication. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,384,7.1
V3,,V3.2,Session Binding,V3.2.2,Verify that session tokens possess at least 64 bits of entropy. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,331,7.1
V3,,V3.2,Session Binding,V3.2.3,Verify the application only stores session tokens in the browser using secure methods such as appropriately secured cookies (see section 3.4) or HTML 5 session storage.,✓,✓,✓,539,7.1
V3,,V3.2,Session Binding,V3.2.4,Verify that session tokens are generated using approved cryptographic algorithms. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,331,7.1
V3,,V3.3,Session Termination,V3.3.1,"Verify that logout and expiration invalidate the session token, such that the back button or a downstream relying party does not resume an authenticated session, including across relying parties. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,613,7.1
V3,,V3.3,Session Termination,V3.3.2,"If authenticators permit users to remain logged in, verify that re-authentication occurs periodically both when actively used or after an idle period. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",30 days,"12 hours or 30 minutes of inactivity, 2FA optional","12 hours or 15 minutes of inactivity, with 2FA",613,7.2
V3,,V3.3,Session Termination,V3.3.3,"Verify that the application gives the option to terminate all other active sessions after a successful password change (including change via password reset/recovery), and that this is effective across the application, federated login (if present), and any relying parties.",,✓,✓,613,
V3,,V3.3,Session Termination,V3.3.4,Verify that users are able to view and (having re-entered login credentials) log out of any or all currently active sessions and devices.,,✓,✓,613,7.1
V3,,V3.4,Cookie-based Session Management,V3.4.1,Verify that cookie-based session tokens have the 'Secure' attribute set. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,614,7.1.1
V3,,V3.4,Cookie-based Session Management,V3.4.2,Verify that cookie-based session tokens have the 'HttpOnly' attribute set. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,1004,7.1.1
V3,,V3.4,Cookie-based Session Management,V3.4.3,Verify that cookie-based session tokens utilize the 'SameSite' attribute to limit exposure to cross-site request forgery attacks. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,16,7.1.1
V3,,V3.4,Cookie-based Session Management,V3.4.4,"Verify that cookie-based session tokens use the ""__Host-"" prefix so cookies are only sent to the host that initially set the cookie.",✓,✓,✓,16,7.1.1
V3,,V3.4,Cookie-based Session Management,V3.4.5,"Verify that if the application is published under a domain name with other applications that set or use session cookies that might disclose the session cookies, set the path attribute in cookie-based session tokens using the most precise path possible. ([C6](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,16,7.1.1
V3,,V3.5,Token-based Session Management,V3.5.1,Verify the application allows users to revoke OAuth tokens that form trust relationships with linked applications.,,✓,✓,290,7.1.2
V3,,V3.5,Token-based Session Management,V3.5.2,"Verify the application uses session tokens rather than static API secrets and keys, except with legacy implementations.",,✓,✓,798,
V3,,V3.5,Token-based Session Management,V3.5.3,"Verify that stateless session tokens use digital signatures, encryption, and other countermeasures to protect against tampering, enveloping, replay, null cipher, and key substitution attacks.",,✓,✓,345,
V3,,V3.6,Federated Re-authentication,V3.6.1,Verify that Relying Parties (RPs) specify the maximum authentication time to Credential Service Providers (CSPs) and that CSPs re-authenticate the user if they haven't used a session within that period.,,,✓,613,7.2.1
V3,,V3.6,Federated Re-authentication,V3.6.2,"Verify that Credential Service Providers (CSPs) inform Relying Parties (RPs) of the last authentication event, to allow RPs to determine if they need to re-authenticate the user.",,,✓,613,7.2.1
V3,,V3.7,Defenses Against Session Management Exploits,V3.7.1,"Verify the application ensures a full, valid login session or requires re-authentication or secondary verification before allowing any sensitive transactions or account modifications.",✓,✓,✓,306,
V4,,V4.1,General Access Control Design,V4.1.1,"Verify that the application enforces access control rules on a trusted service layer, especially if client-side access control is present and could be bypassed.",✓,✓,✓,602,
V4,,V4.1,General Access Control Design,V4.1.2,Verify that all user and data attributes and policy information used by access controls cannot be manipulated by end users unless specifically authorized.,✓,✓,✓,639,
V4,,V4.1,General Access Control Design,V4.1.3,"Verify that the principle of least privilege exists - users should only be able to access functions, data files, URLs, controllers, services, and other resources, for which they possess specific authorization. This implies protection against spoofing and elevation of privilege. ([C7](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,285,
V4,,V4.1,General Access Control Design,V4.1.4,"[DELETED, DUPLICATE OF 4.1.3]",,,,,
V4,,V4.1,General Access Control Design,V4.1.5,Verify that access controls fail securely including when an exception occurs. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,285,
V4,,V4.2,Operation Level Access Control,V4.2.1,"Verify that sensitive data and APIs are protected against Insecure Direct Object Reference (IDOR) attacks targeting creation, reading, updating and deletion of records, such as creating or updating someone else's record, viewing everyone's records, or deleting all records.",✓,✓,✓,639,
V4,,V4.2,Operation Level Access Control,V4.2.2,"Verify that the application or framework enforces a strong anti-CSRF mechanism to protect authenticated functionality, and effective anti-automation or anti-CSRF protects unauthenticated functionality.",✓,✓,✓,352,
V4,,V4.3,Other Access Control Considerations,V4.3.1,Verify administrative interfaces use appropriate multi-factor authentication to prevent unauthorized use.,✓,✓,✓,419,
V4,,V4.3,Other Access Control Considerations,V4.3.2,"Verify that directory browsing is disabled unless deliberately desired. Additionally, applications should not allow discovery or disclosure of file or directory metadata, such as Thumbs.db, .DS_Store, .git or .svn folders.",✓,✓,✓,548,
V4,,V4.3,Other Access Control Considerations,V4.3.3,"Verify the application has additional authorization (such as step up or adaptive authentication) for lower value systems, and / or segregation of duties for high value applications to enforce anti-fraud controls as per the risk of application and past fraud.",,✓,✓,732,
V5,,V5.1,Input Validation,V5.1.1,"Verify that the application has defenses against HTTP parameter pollution attacks, particularly if the application framework makes no distinction about the source of request parameters (GET, POST, cookies, headers, or environment variables).",✓,✓,✓,235,
V5,,V5.1,Input Validation,V5.1.2,"Verify that frameworks protect against mass parameter assignment attacks, or that the application has countermeasures to protect against unsafe parameter assignment, such as marking fields private or similar. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,915,
V5,,V5.1,Input Validation,V5.1.3,"Verify that all input (HTML form fields, REST requests, URL parameters, HTTP headers, cookies, batch files, RSS feeds, etc) is validated using positive validation (allow lists). ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,20,
V5,,V5.1,Input Validation,V5.1.4,"Verify that structured data is strongly typed and validated against a defined schema including allowed characters, length and pattern (e.g. credit card numbers, e-mail addresses, telephone numbers, or validating that two related fields are reasonable, such as checking that suburb and zip/postcode match). ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,20,
V5,,V5.1,Input Validation,V5.1.5,"Verify that URL redirects and forwards only allow destinations which appear on an allow list, or show a warning when redirecting to potentially untrusted content.",✓,✓,✓,601,
V5,,V5.2,Sanitization and Sandboxing,V5.2.1,Verify that all untrusted HTML input from WYSIWYG editors or similar is properly sanitized with an HTML sanitizer library or framework feature. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,116,
V5,,V5.2,Sanitization and Sandboxing,V5.2.2,Verify that unstructured data is sanitized to enforce safety measures such as allowed characters and length.,✓,✓,✓,138,
V5,,V5.2,Sanitization and Sandboxing,V5.2.3,Verify that the application sanitizes user input before passing to mail systems to protect against SMTP or IMAP injection.,✓,✓,✓,147,
V5,,V5.2,Sanitization and Sandboxing,V5.2.4,"Verify that the application avoids the use of eval() or other dynamic code execution features. Where there is no alternative, any user input being included must be sanitized or sandboxed before being executed.",✓,✓,✓,95,
V5,,V5.2,Sanitization and Sandboxing,V5.2.5,Verify that the application protects against template injection attacks by ensuring that any user input being included is sanitized or sandboxed.,✓,✓,✓,94,
V5,,V5.2,Sanitization and Sandboxing,V5.2.6,"Verify that the application protects against SSRF attacks, by validating or sanitizing untrusted data or HTTP file metadata, such as filenames and URL input fields, and uses allow lists of protocols, domains, paths and ports.",✓,✓,✓,918,
V5,,V5.2,Sanitization and Sandboxing,V5.2.7,"Verify that the application sanitizes, disables, or sandboxes user-supplied Scalable Vector Graphics (SVG) scriptable content, especially as they relate to XSS resulting from inline scripts, and foreignObject.",✓,✓,✓,159,
V5,,V5.2,Sanitization and Sandboxing,V5.2.8,"Verify that the application sanitizes, disables, or sandboxes user-supplied scriptable or expression template language content, such as Markdown, CSS or XSL stylesheets, BBCode, or similar.",✓,✓,✓,94,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.1,"Verify that output encoding is relevant for the interpreter and context required. For example, use encoders specifically for HTML values, HTML attributes, JavaScript, URL parameters, HTTP headers, SMTP, and others as the context requires, especially from untrusted inputs (e.g. names with Unicode or apostrophes, such as ねこ or O'Hara). ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,116,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.2,"Verify that output encoding preserves the user's chosen character set and locale, such that any Unicode character point is valid and safely handled. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,176,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.3,"Verify that context-aware, preferably automated - or at worst, manual - output escaping protects against reflected, stored, and DOM based XSS. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,79,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.4,"Verify that data selection or database queries (e.g. SQL, HQL, ORM, NoSQL) use parameterized queries, ORMs, entity frameworks, or are otherwise protected from database injection attacks. ([C3](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,89,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.5,"Verify that where parameterized or safer mechanisms are not present, context-specific output encoding is used to protect against injection attacks, such as the use of SQL escaping to protect against SQL injection. ([C3, C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,89,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.6,"Verify that the application protects against JSON injection attacks, JSON eval attacks, and JavaScript expression evaluation. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,830,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.7,"Verify that the application protects against LDAP injection vulnerabilities, or that specific security controls to prevent LDAP injection have been implemented. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,90,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.8,Verify that the application protects against OS command injection and that operating system calls use parameterized OS queries or use contextual command line output encoding. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,78,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.9,Verify that the application protects against Local File Inclusion (LFI) or Remote File Inclusion (RFI) attacks.,✓,✓,✓,829,
V5,,V5.3,Output Encoding and Injection Prevention,V5.3.10,Verify that the application protects against XPath injection or XML injection attacks. ([C4](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,643,
V5,,V5.4,"Memory, String, and Unmanaged Code",V5.4.1,"Verify that the application uses memory-safe string, safer memory copy and pointer arithmetic to detect or prevent stack, buffer, or heap overflows.",,✓,✓,120,
V5,,V5.4,"Memory, String, and Unmanaged Code",V5.4.2,"Verify that format strings do not take potentially hostile input, and are constant.",,✓,✓,134,
V5,,V5.4,"Memory, String, and Unmanaged Code",V5.4.3,"Verify that sign, range, and input validation techniques are used to prevent integer overflows.",,✓,✓,190,
V5,,V5.5,Deserialization Prevention,V5.5.1,Verify that serialized objects use integrity checks or are encrypted to prevent hostile object creation or data tampering. ([C5](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,502,
V5,,V5.5,Deserialization Prevention,V5.5.2,Verify that the application correctly restricts XML parsers to only use the most restrictive configuration possible and to ensure that unsafe features such as resolving external entities are disabled to prevent XML eXternal Entity (XXE) attacks.,✓,✓,✓,611,
V5,,V5.5,Deserialization Prevention,V5.5.3,"Verify that deserialization of untrusted data is avoided or is protected in both custom code and third-party libraries (such as JSON, XML and YAML parsers).",✓,✓,✓,502,
V5,,V5.5,Deserialization Prevention,V5.5.4,"Verify that when parsing JSON in browsers or JavaScript-based backends, JSON.parse is used to parse the JSON document. Do not use eval() to parse JSON.",✓,✓,✓,95,
V6,,V6.1,Data Classification,V6.1.1,"Verify that regulated private data is stored encrypted while at rest, such as Personally Identifiable Information (PII), sensitive personal information, or data assessed likely to be subject to EU's GDPR.",,✓,✓,311,
V6,,V6.1,Data Classification,V6.1.2,"Verify that regulated health data is stored encrypted while at rest, such as medical records, medical device details, or de-anonymized research records.",,✓,✓,311,
V6,,V6.1,Data Classification,V6.1.3,"Verify that regulated financial data is stored encrypted while at rest, such as financial accounts, defaults or credit history, tax records, pay history, beneficiaries, or de-anonymized market or research records.",,✓,✓,311,
V6,,V6.2,Algorithms,V6.2.1,"Verify that all cryptographic modules fail securely, and errors are handled in a way that does not enable Padding Oracle attacks.",✓,✓,✓,310,
V6,,V6.2,Algorithms,V6.2.2,"Verify that industry proven or government approved cryptographic algorithms, modes, and libraries are used, instead of custom coded cryptography. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,327,
V6,,V6.2,Algorithms,V6.2.3,"Verify that encryption initialization vector, cipher configuration, and block modes are configured securely using the latest advice.",,✓,✓,326,
V6,,V6.2,Algorithms,V6.2.4,"Verify that random number, encryption or hashing algorithms, key lengths, rounds, ciphers or modes, can be reconfigured, upgraded, or swapped at any time, to protect against cryptographic breaks. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,326,
V6,,V6.2,Algorithms,V6.2.5,"Verify that known insecure block modes (i.e. ECB, etc.), padding modes (i.e. PKCS#1 v1.5, etc.), ciphers with small block sizes (i.e. Triple-DES, Blowfish, etc.), and weak hashing algorithms (i.e. MD5, SHA1, etc.) are not used unless required for backwards compatibility.",,✓,✓,326,
V6,,V6.2,Algorithms,V6.2.6,"Verify that nonces, initialization vectors, and other single use numbers must not be used more than once with a given encryption key. The method of generation must be appropriate for the algorithm being used.",,✓,✓,326,
V6,,V6.2,Algorithms,V6.2.7,"Verify that encrypted data is authenticated via signatures, authenticated cipher modes, or HMAC to ensure that ciphertext is not altered by an unauthorized party.",,,✓,326,
V6,,V6.2,Algorithms,V6.2.8,"Verify that all cryptographic operations are constant-time, with no 'short-circuit' operations in comparisons, calculations, or returns, to avoid leaking information.",,,✓,385,
V6,,V6.3,Random Values,V6.3.1,"Verify that all random numbers, random file names, random GUIDs, and random strings are generated using the cryptographic module's approved cryptographically secure random number generator when these random values are intended to be not guessable by an attacker.",,✓,✓,338,
V6,,V6.3,Random Values,V6.3.2,"Verify that random GUIDs are created using the GUID v4 algorithm, and a Cryptographically-secure Pseudo-random Number Generator (CSPRNG). GUIDs created using other pseudo-random number generators may be predictable.",,✓,✓,338,
V6,,V6.3,Random Values,V6.3.3,"Verify that random numbers are created with proper entropy even when the application is under heavy load, or that the application degrades gracefully in such circumstances.",,,✓,338,
V6,,V6.4,Secret Management,V6.4.1,"Verify that a secrets management solution such as a key vault is used to securely create, store, control access to and destroy secrets. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,798,
V6,,V6.4,Secret Management,V6.4.2,Verify that key material is not exposed to the application but instead uses an isolated security module like a vault for cryptographic operations. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,320,
V7,,V7.1,Log Content,V7.1.1,"Verify that the application does not log credentials or payment details. Session tokens should only be stored in logs in an irreversible, hashed form. ([C9, C10](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,532,
V7,,V7.1,Log Content,V7.1.2,Verify that the application does not log other sensitive data as defined under local privacy laws or relevant security policy. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),✓,✓,✓,532,
V7,,V7.1,Log Content,V7.1.3,"Verify that the application logs security relevant events including successful and failed authentication events, access control failures, deserialization failures and input validation failures. ([C5, C7](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,778,
V7,,V7.1,Log Content,V7.1.4,Verify that each log event includes necessary information that would allow for a detailed investigation of the timeline when an event happens. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,778,
V7,,V7.2,Log Processing,V7.2.1,"Verify that all authentication decisions are logged, without storing sensitive session tokens or passwords. This should include requests with relevant metadata needed for security investigations.",,✓,✓,778,
V7,,V7.2,Log Processing,V7.2.2,Verify that all access control decisions can be logged and all failed decisions are logged. This should include requests with relevant metadata needed for security investigations.,,✓,✓,285,
V7,,V7.3,Log Protection,V7.3.1,Verify that all logging components appropriately encode data to prevent log injection. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,117,
V7,,V7.3,Log Protection,V7.3.2,"[DELETED, DUPLICATE OF 7.3.1]",,,,,
V7,,V7.3,Log Protection,V7.3.3,Verify that security logs are protected from unauthorized access and modification. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,200,
V7,,V7.3,Log Protection,V7.3.4,Verify that time sources are synchronized to the correct time and time zone. Strongly consider logging only in UTC if systems are global to assist with post-incident forensic analysis. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,,
V7,,V7.4,Error Handling,V7.4.1,"Verify that a generic message is shown when an unexpected or security sensitive error occurs, potentially with a unique ID which support personnel can use to investigate. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,210,
V7,,V7.4,Error Handling,V7.4.2,Verify that exception handling (or a functional equivalent) is used across the codebase to account for expected and unexpected error conditions. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,544,
V7,,V7.4,Error Handling,V7.4.3,"Verify that a ""last resort"" error handler is defined which will catch all unhandled exceptions. ([C10](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,431,
V8,,V8.1,General Data Protection,V8.1.1,Verify the application protects sensitive data from being cached in server components such as load balancers and application caches.,,✓,✓,524,
V8,,V8.1,General Data Protection,V8.1.2,Verify that all cached or temporary copies of sensitive data stored on the server are protected from unauthorized access or purged/invalidated after the authorized user accesses the sensitive data.,,✓,✓,524,
V8,,V8.1,General Data Protection,V8.1.3,"Verify the application minimizes the number of parameters in a request, such as hidden fields, Ajax variables, cookies and header values.",,✓,✓,233,
V8,,V8.1,General Data Protection,V8.1.4,"Verify the application can detect and alert on abnormal numbers of requests, such as by IP, user, total per hour or day, or whatever makes sense for the application.",,✓,✓,770,
V8,,V8.1,General Data Protection,V8.1.5,Verify that regular backups of important data are performed and that test restoration of data is performed.,,,✓,19,
V8,,V8.1,General Data Protection,V8.1.6,Verify that backups are stored securely to prevent data from being stolen or corrupted.,,,✓,19,
V8,,V8.2,Client-side Data Protection,V8.2.1,Verify the application sets sufficient anti-caching headers so that sensitive data is not cached in modern browsers.,✓,✓,✓,525,
V8,,V8.2,Client-side Data Protection,V8.2.2,"Verify that data stored in browser storage (such as localStorage, sessionStorage, IndexedDB, or cookies) does not contain sensitive data.",✓,✓,✓,922,
V8,,V8.2,Client-side Data Protection,V8.2.3,"Verify that authenticated data is cleared from client storage, such as the browser DOM, after the client or session is terminated.",✓,✓,✓,922,
V8,,V8.3,Sensitive Private Data,V8.3.1,"Verify that sensitive data is sent to the server in the HTTP message body or headers, and that query string parameters from any HTTP verb do not contain sensitive data.",✓,✓,✓,319,
V8,,V8.3,Sensitive Private Data,V8.3.2,Verify that users have a method to remove or export their data on demand.,✓,✓,✓,212,
V8,,V8.3,Sensitive Private Data,V8.3.3,Verify that users are provided clear language regarding collection and use of supplied personal information and that users have provided opt-in consent for the use of that data before it is used in any way.,✓,✓,✓,285,
V8,,V8.3,Sensitive Private Data,V8.3.4,"Verify that all sensitive data created and processed by the application has been identified, and ensure that a policy is in place on how to deal with sensitive data. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,200,
V8,,V8.3,Sensitive Private Data,V8.3.5,"Verify accessing sensitive data is audited (without logging the sensitive data itself), if the data is collected under relevant data protection directives or where logging of access is required.",,✓,✓,532,
V8,,V8.3,Sensitive Private Data,V8.3.6,"Verify that sensitive information contained in memory is overwritten as soon as it is no longer required to mitigate memory dumping attacks, using zeroes or random data.",,✓,✓,226,
V8,,V8.3,Sensitive Private Data,V8.3.7,"Verify that sensitive or private information that is required to be encrypted, is encrypted using approved algorithms that provide both confidentiality and integrity. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,327,
V8,,V8.3,Sensitive Private Data,V8.3.8,"Verify that sensitive personal information is subject to data retention classification, such that old or out of date data is deleted automatically, on a schedule, or as the situation requires.",,✓,✓,285,
V9,,V9.1,Client Communication Security,V9.1.1,"Verify that TLS is used for all client connectivity, and does not fall back to insecure or unencrypted communications. ([C8](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,319,
V9,,V9.1,Client Communication Security,V9.1.2,"Verify using up to date TLS testing tools that only strong cipher suites are enabled, with the strongest cipher suites set as preferred.",✓,✓,✓,326,
V9,,V9.1,Client Communication Security,V9.1.3,"Verify that only the latest recommended versions of the TLS protocol are enabled, such as TLS 1.2 and TLS 1.3. The latest version of the TLS protocol should be the preferred option.",✓,✓,✓,326,
V9,,V9.2,Server Communication Security,V9.2.1,"Verify that connections to and from the server use trusted TLS certificates. Where internally generated or self-signed certificates are used, the server must be configured to only trust specific internal CAs and specific self-signed certificates. All others should be rejected.",,✓,✓,295,
V9,,V9.2,Server Communication Security,V9.2.2,"Verify that encrypted communications such as TLS is used for all inbound and outbound connections, including for management ports, monitoring, authentication, API, or web service calls, database, cloud, serverless, mainframe, external, and partner connections. The server must not fall back to insecure or unencrypted protocols.",,✓,✓,319,
V9,,V9.2,Server Communication Security,V9.2.3,Verify that all encrypted connections to external systems that involve sensitive information or functions are authenticated.,,✓,✓,287,
V9,,V9.2,Server Communication Security,V9.2.4,"Verify that proper certification revocation, such as Online Certificate Status Protocol (OCSP) Stapling, is enabled and configured.",,✓,✓,299,
V9,,V9.2,Server Communication Security,V9.2.5,Verify that backend TLS connection failures are logged.,,,✓,544,
V10,,V10.1,Code Integrity,V10.1.1,"Verify that a code analysis tool is in use that can detect potentially malicious code, such as time functions, unsafe file operations and network connections.",,,✓,749,
V10,,V10.2,Malicious Code Search,V10.2.1,"Verify that the application source code and third party libraries do not contain unauthorized phone home or data collection capabilities. Where such functionality exists, obtain the user's permission for it to operate before collecting any data.",,✓,✓,359,
V10,,V10.2,Malicious Code Search,V10.2.2,"Verify that the application does not ask for unnecessary or excessive permissions to privacy related features or sensors, such as contacts, cameras, microphones, or location.",,✓,✓,272,
V10,,V10.2,Malicious Code Search,V10.2.3,"Verify that the application source code and third party libraries do not contain back doors, such as hard-coded or additional undocumented accounts or keys, code obfuscation, undocumented binary blobs, rootkits, or anti-debugging, insecure debugging features, or otherwise out of date, insecure, or hidden functionality that could be used maliciously if discovered.",,,✓,507,
V10,,V10.2,Malicious Code Search,V10.2.4,Verify that the application source code and third party libraries do not contain time bombs by searching for date and time related functions.,,,✓,511,
V10,,V10.2,Malicious Code Search,V10.2.5,"Verify that the application source code and third party libraries do not contain malicious code, such as salami attacks, logic bypasses, or logic bombs.",,,✓,511,
V10,,V10.2,Malicious Code Search,V10.2.6,Verify that the application source code and third party libraries do not contain Easter eggs or any other potentially unwanted functionality.,,,✓,507,
V10,,V10.3,Application Integrity,V10.3.1,"Verify that if the application has a client or server auto-update feature, updates should be obtained over secure channels and digitally signed. The update code must validate the digital signature of the update before installing or executing the update.",✓,✓,✓,16,
V10,,V10.3,Application Integrity,V10.3.2,"Verify that the application employs integrity protections, such as code signing or subresource integrity. The application must not load or execute code from untrusted sources, such as loading includes, modules, plugins, code, or libraries from untrusted sources or the Internet.",✓,✓,✓,353,
V10,,V10.3,Application Integrity,V10.3.3,"Verify that the application has protection from subdomain takeovers if the application relies upon DNS entries or DNS subdomains, such as expired domain names, out of date DNS pointers or CNAMEs, expired projects at public source code repos, or transient cloud APIs, serverless functions, or storage buckets (*autogen-bucket-id*.cloud.example.com) or similar. Protections can include ensuring that DNS names used by applications are regularly checked for expiry or change.",✓,✓,✓,350,
V11,,V11.1,Business Logic Security,V11.1.1,Verify that the application will only process business logic flows for the same user in sequential step order and without skipping steps.,✓,✓,✓,841,
V11,,V11.1,Business Logic Security,V11.1.2,"Verify that the application will only process business logic flows with all steps being processed in realistic human time, i.e. transactions are not submitted too quickly.",✓,✓,✓,799,
V11,,V11.1,Business Logic Security,V11.1.3,Verify the application has appropriate limits for specific business actions or transactions which are correctly enforced on a per user basis.,✓,✓,✓,770,
V11,,V11.1,Business Logic Security,V11.1.4,"Verify that the application has anti-automation controls to protect against excessive calls such as mass data exfiltration, business logic requests, file uploads or denial of service attacks.",✓,✓,✓,770,
V11,,V11.1,Business Logic Security,V11.1.5,"Verify the application has business logic limits or validation to protect against likely business risks or threats, identified using threat modeling or similar methodologies.",✓,✓,✓,841,
V11,,V11.1,Business Logic Security,V11.1.6,"Verify that the application does not suffer from ""Time Of Check to Time Of Use"" (TOCTOU) issues or other race conditions for sensitive operations.",,✓,✓,367,
V11,,V11.1,Business Logic Security,V11.1.7,"Verify that the application monitors for unusual events or activity from a business logic perspective. For example, attempts to perform actions out of order or actions which a normal user would never attempt. ([C9](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,754,
V11,,V11.1,Business Logic Security,V11.1.8,Verify that the application has configurable alerting when automated attacks or unusual activity is detected.,,✓,✓,390,
V12,,V12.1,File Upload,V12.1.1,Verify that the application will not accept large files that could fill up storage or cause a denial of service.,✓,✓,✓,400,
V12,,V12.1,File Upload,V12.1.2,"Verify that the application checks compressed files (e.g. zip, gz, docx, odt) against maximum allowed uncompressed size and against maximum number of files before uncompressing the file.",,✓,✓,409,
V12,,V12.1,File Upload,V12.1.3,"Verify that a file size quota and maximum number of files per user is enforced to ensure that a single user cannot fill up the storage with too many files, or excessively large files.",,✓,✓,770,
V12,,V12.2,File Integrity,V12.2.1,Verify that files obtained from untrusted sources are validated to be of expected type based on the file's content.,,✓,✓,434,
V12,,V12.3,File Execution,V12.3.1,Verify that user-submitted filename metadata is not used directly by system or framework filesystems and that a URL API is used to protect against path traversal.,✓,✓,✓,22,
V12,,V12.3,File Execution,V12.3.2,"Verify that user-submitted filename metadata is validated or ignored to prevent the disclosure, creation, updating or removal of local files (LFI).",✓,✓,✓,73,
V12,,V12.3,File Execution,V12.3.3,Verify that user-submitted filename metadata is validated or ignored to prevent the disclosure or execution of remote files via Remote File Inclusion (RFI) or Server-side Request Forgery (SSRF) attacks.,✓,✓,✓,98,
V12,,V12.3,File Execution,V12.3.4,"Verify that the application protects against Reflective File Download (RFD) by validating or ignoring user-submitted filenames in a JSON, JSONP, or URL parameter, the response Content-Type header should be set to text/plain, and the Content-Disposition header should have a fixed filename.",✓,✓,✓,641,
V12,,V12.3,File Execution,V12.3.5,"Verify that untrusted file metadata is not used directly with system API or libraries, to protect against OS command injection.",✓,✓,✓,78,
V12,,V12.3,File Execution,V12.3.6,"Verify that the application does not include and execute functionality from untrusted sources, such as unverified content distribution networks, JavaScript libraries, node npm libraries, or server-side DLLs.",,✓,✓,829,
V12,,V12.4,File Storage,V12.4.1,"Verify that files obtained from untrusted sources are stored outside the web root, with limited permissions.",✓,✓,✓,552,
V12,,V12.4,File Storage,V12.4.2,Verify that files obtained from untrusted sources are scanned by antivirus scanners to prevent upload and serving of known malicious content.,✓,✓,✓,509,
V12,,V12.5,File Download,V12.5.1,"Verify that the web tier is configured to serve only files with specific file extensions to prevent unintentional information and source code leakage. For example, backup files (e.g. .bak), temporary working files (e.g. .swp), compressed files (.zip, .tar.gz, etc) and other extensions commonly used by editors should be blocked unless required.",✓,✓,✓,552,
V12,,V12.5,File Download,V12.5.2,Verify that direct requests to uploaded files will never be executed as HTML/JavaScript content.,✓,✓,✓,434,
V12,,V12.6,SSRF Protection,V12.6.1,Verify that the web or application server is configured with an allow list of resources or systems to which the server can send requests or load data/files from.,✓,✓,✓,918,
V13,,V13.1,Generic Web Service Security,V13.1.1,Verify that all application components use the same encodings and parsers to avoid parsing attacks that exploit different URI or file parsing behavior that could be used in SSRF and RFI attacks.,✓,✓,✓,116,
V13,,V13.1,Generic Web Service Security,V13.1.2,"[DELETED, DUPLICATE OF 4.3.1]",,,,,
V13,,V13.1,Generic Web Service Security,V13.1.3,"Verify API URLs do not expose sensitive information, such as the API key, session tokens etc.",✓,✓,✓,598,
V13,,V13.1,Generic Web Service Security,V13.1.4,"Verify that authorization decisions are made at both the URI, enforced by programmatic or declarative security at the controller or router, and at the resource level, enforced by model-based permissions.",,✓,✓,285,
V13,,V13.1,Generic Web Service Security,V13.1.5,Verify that requests containing unexpected or missing content types are rejected with appropriate headers (HTTP response status 406 Unacceptable or 415 Unsupported Media Type).,,✓,✓,434,
V13,,V13.2,RESTful Web Service,V13.2.1,"Verify that enabled RESTful HTTP methods are a valid choice for the user or action, such as preventing normal users using DELETE or PUT on protected API or resources.",✓,✓,✓,650,
V13,,V13.2,RESTful Web Service,V13.2.2,Verify that JSON schema validation is in place and verified before accepting input.,✓,✓,✓,20,
V13,,V13.2,RESTful Web Service,V13.2.3,"Verify that RESTful web services that utilize cookies are protected from Cross-Site Request Forgery via the use of at least one or more of the following: double submit cookie pattern, CSRF nonces, or Origin request header checks.",✓,✓,✓,352,
V13,,V13.2,RESTful Web Service,V13.2.4,"[DELETED, DUPLICATE OF 11.1.4]",,,,,
V13,,V13.2,RESTful Web Service,V13.2.5,"Verify that REST services explicitly check the incoming Content-Type to be the expected one, such as application/xml or application/json.",,✓,✓,436,
V13,,V13.2,RESTful Web Service,V13.2.6,Verify that the message headers and payload are trustworthy and not modified in transit. Requiring strong encryption for transport (TLS only) may be sufficient in many cases as it provides both confidentiality and integrity protection. Per-message digital signatures can provide additional assurance on top of the transport protections for high-security applications but bring with them additional complexity and risks to weigh against the benefits.,,✓,✓,345,
V13,,V13.3,SOAP Web Service,V13.3.1,"Verify that XSD schema validation takes place to ensure a properly formed XML document, followed by validation of each input field before any processing of that data takes place.",✓,✓,✓,20,
V13,,V13.3,SOAP Web Service,V13.3.2,Verify that the message payload is signed using WS-Security to ensure reliable transport between client and service.,,✓,✓,345,
V13,,V13.4,GraphQL,V13.4.1,"Verify that a query allow list or a combination of depth limiting and amount limiting is used to prevent GraphQL or data layer expression Denial of Service (DoS) as a result of expensive, nested queries. For more advanced scenarios, query cost analysis should be used.",,✓,✓,770,
V13,,V13.4,GraphQL,V13.4.2,Verify that GraphQL or other data layer authorization logic should be implemented at the business logic layer instead of the GraphQL layer.,,✓,✓,285,
V14,,V14.1,Build and Deploy,V14.1.1,"Verify that the application build and deployment processes are performed in a secure and repeatable way, such as CI / CD automation, automated configuration management, and automated deployment scripts.",,✓,✓,,
V14,,V14.1,Build and Deploy,V14.1.2,"Verify that compiler flags are configured to enable all available buffer overflow protections and warnings, including stack randomization, data execution prevention, and to break the build if an unsafe pointer, memory, format string, integer, or string operations are found.",,✓,✓,120,
V14,,V14.1,Build and Deploy,V14.1.3,Verify that server configuration is hardened as per the recommendations of the application server and frameworks in use.,,✓,✓,16,
V14,,V14.1,Build and Deploy,V14.1.4,"Verify that the application, configuration, and all dependencies can be re-deployed using automated deployment scripts, built from a documented and tested runbook in a reasonable time, or restored from backups in a timely fashion.",,✓,✓,,
V14,,V14.1,Build and Deploy,V14.1.5,Verify that authorized administrators can verify the integrity of all security-relevant configurations to detect tampering.,,,✓,,
V14,,V14.2,Dependency,V14.2.1,"Verify that all components are up to date, preferably using a dependency checker during build or compile time. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))",✓,✓,✓,1026,
V14,,V14.2,Dependency,V14.2.2,"Verify that all unneeded features, documentation, sample applications and configurations are removed.",✓,✓,✓,1002,
V14,,V14.2,Dependency,V14.2.3,"Verify that if application assets, such as JavaScript libraries, CSS or web fonts, are hosted externally on a Content Delivery Network (CDN) or external provider, Subresource Integrity (SRI) is used to validate the integrity of the asset.",✓,✓,✓,829,
V14,,V14.2,Dependency,V14.2.4,"Verify that third party components come from pre-defined, trusted and continually maintained repositories. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering))",,✓,✓,829,
V14,,V14.2,Dependency,V14.2.5,Verify that a Software Bill of Materials (SBOM) is maintained of all third party libraries in use. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,,
V14,,V14.2,Dependency,V14.2.6,Verify that the attack surface is reduced by sandboxing or encapsulating third party libraries to expose only the required behaviour into the application. ([C2](https://owasp.org/www-project-proactive-controls/#div-numbering)),,✓,✓,265,
V14,,V14.3,Unintended Security Disclosure,V14.3.1,"[DELETED, DUPLICATE OF 7.4.1]",,,,,
V14,,V14.3,Unintended Security Disclosure,V14.3.2,"Verify that web or application server and application framework debug modes are disabled in production to eliminate debug features, developer consoles, and unintended security disclosures.",✓,✓,✓,497,
V14,,V14.3,Unintended Security Disclosure,V14.3.3,Verify that the HTTP headers or any part of the HTTP response do not expose detailed version information of system components.,✓,✓,✓,200,
V14,,V14.4,HTTP Security Headers,V14.4.1,"Verify that every HTTP response contains a Content-Type header. Also specify a safe character set (e.g., UTF-8, ISO-8859-1) if the content types are text/*, /+xml and application/xml. Content must match with the provided Content-Type header.",✓,✓,✓,173,
V14,,V14.4,HTTP Security Headers,V14.4.2,"Verify that all API responses contain a Content-Disposition: attachment; filename=""api.json"" header (or other appropriate filename for the content type).",✓,✓,✓,116,
V14,,V14.4,HTTP Security Headers,V14.4.3,"Verify that a Content Security Policy (CSP) response header is in place that helps mitigate impact for XSS attacks like HTML, DOM, JSON, and JavaScript injection vulnerabilities.",✓,✓,✓,1021,
V14,,V14.4,HTTP Security Headers,V14.4.4,Verify that all responses contain a X-Content-Type-Options: nosniff header.,✓,✓,✓,116,
V14,,V14.4,HTTP Security Headers,V14.4.5,"Verify that a Strict-Transport-Security header is included on all responses and for all subdomains, such as Strict-Transport-Security: max-age=15724800; includeSubdomains.",✓,✓,✓,523,
V14,,V14.4,HTTP Security Headers,V14.4.6,Verify that a suitable Referrer-Policy header is included to avoid exposing sensitive information in the URL through the Referer header to untrusted parties.,✓,✓,✓,116,
V14,,V14.4,HTTP Security Headers,V14.4.7,Verify that the content of a web application cannot be embedded in a third-party site by default and that embedding of the exact resources is only allowed where necessary by using suitable Content-Security-Policy: frame-ancestors and X-Frame-Options response headers.,✓,✓,✓,1021,
V14,,V14.5,HTTP Request Header Validation,V14.5.1,"Verify that the application server only accepts the HTTP methods in use by the application/API, including pre-flight OPTIONS, and logs/alerts on any requests that are not valid for the application context.",✓,✓,✓,749,
V14,,V14.5,HTTP Request Header Validation,V14.5.2,"Verify that the supplied Origin header is not used for authentication or access control decisions, as the Origin header can easily be changed by an attacker.",✓,✓,✓,346,
V14,,V14.5,HTTP Request Header Validation,V14.5.3,"Verify that the Cross-Origin Resource Sharing (CORS) Access-Control-Allow-Origin header uses a strict allow list of trusted domains and subdomains to match against and does not support the ""null"" origin.",✓,✓,✓,346,
V14,,V14.5,HTTP Request Header Validation,V14.5.4,"Verify that HTTP headers added by a trusted proxy or SSO devices, such as a bearer token, are authenticated by the application.",,✓,✓,306,
'''
        return csv_content
    elif csvType == "failed logins":
        csv_content = '''Analyzed Client IP,DB User Name,OS User,Server IP,Sender IP,Server Host Name,Service Name,Source Program,Server Type,Database Name,Client Host Name,Database Error Text,Error Code,Exception Type Description,Count of Exceptions
10.87.5.22,?,WASADM,136.61.213.99,136.61.212.62,AQP6PL1000N2-SCAN.ID.AAA,QIHHHVA1_APP.ID.AAA,JDBC THIN CLIENT,ORACLE,,,,,Login Failed,3590517
10.87.5.22,?,WASADM,136.61.213.98,136.61.212.62,,QIHHHVA1_APP.ID.AAA,JDBC THIN CLIENT,ORACLE,,,,,Login Failed,3590510
10.87.5.22,?,WASADM,136.61.213.97,136.61.212.67,ADP6PL1000N2-SCAN.ID.AAA,QIHHHVA1_APP.ID.AAA,JDBC THIN CLIENT,ORACLE,,,,,Login Failed,3590465
136.61.212.62,SYS,ORACLE,136.61.212.62,136.61.212.62,ADP6PL1000,PIDHEAC11,ORAAGENT.BIN,ORACLE,,DUMMYNAME45,timeout or end-of-fetch during message dequeue from .,ORA-25228,Database Server returned an error,6745
136.60.214.34,?,PATROLAG,136.61.212.181,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1428
136.60.214.34,?,PATROLAG,136.61.212.182,136.61.212.130,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1428
136.60.214.34,?,PATROLAG,136.61.212.181,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1428
136.60.214.34,?,PATROLAG,136.61.212.180,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1428
136.60.214.34,?,PATROLAG,136.61.212.182,136.61.212.130,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1428
136.60.214.34,?,PATROLAG,136.61.212.180,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Login Failed,1427
136.61.212.129,?,,136.61.212.129,136.61.212.129,AQP6PO06,ORACLE,,ORACLE,,DUMMYNAME45,,,Missing Login Information,7
136.61.212.62,?,,136.61.212.62,136.61.212.62,AQP6PL1000,ORACLE,,ORACLE,,DUMMYNAME45,,,Missing Login Information,4
136.61.212.129,SYS,ORACLE,136.61.212.129,136.61.212.129,AQP6PO06,ORACLEPIDWDSD11,RMAN,ORACLE,,DUMMYNAME45,,,Session Error,4
136.60.214.34,?,PATROLAG,136.61.212.181,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,DUMMYNAME45,,,Session Error,4
10.87.22.21,?,,136.61.213.95,136.61.212.62,ADP6PL1000,ORACLE,,ORACLE,,AQL20050608.ID.AAA,,,Missing Login Information,3
136.60.214.34,?,PATROLAG,136.61.212.182,136.61.212.130,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,3
136.60.214.34,?,PATROLAG,136.61.212.180,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,3
136.61.212.129,SYS,ORACLE,136.61.212.129,136.61.212.129,AQP6PO06,ORACLEPIDWPCD11,RMAN,ORACLE,,AQP6PO06,,,Session Error,3
136.60.214.34,?,PATROLAG,136.61.212.180,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,3
136.60.214.34,?,PATROLAG,136.61.212.182,136.61.212.130,AQP6PO06N2-SCAN.ID.AAA,AADRPPD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,3
136.61.212.129,SYS,ORACLE,136.61.212.129,136.61.212.129,AQP6PO06,ORACLEPIDSFPD11,RMAN,ORACLE,,AQP6PO06,,,Session Error,3
10.87.22.23,?,,136.61.213.95,136.61.212.62,ADP6PL1000,ORACLE,,ORACLE,,AQL20050610,,,Missing Login Information,2
10.87.22.21,?,,136.61.213.95,136.61.212.62,ADP6PL1000,ORACLE,,ORACLE,,AQL20050608.ID.AAA,,,Session Error,2
136.61.212.178,PATASMMON,PATROLAG,136.61.212.178,136.61.212.129,AQP6PO06,#NAME?,JDBC THIN CLIENT,ORACLE,,AQP6PO06,,,Session Error,2
136.60.214.34,?,PATROLAG,136.61.212.181,136.61.212.129,AQP6PO06N2-SCAN.ID.AAA,PIDIDSD1.ID.AAA,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,2
10.87.22.22,?,,136.61.213.96,136.61.212.67,AQP6PL1005,ORACLE,,ORACLE,,AQL20050609.ID.AAA,,,Missing Login Information,1
10.87.22.23,?,,136.61.213.96,136.61.212.67,AQP6PL1005,ORACLE,,ORACLE,,AQL20050610,,,Missing Login Information,1
10.87.22.22,?,,136.61.213.95,136.61.212.62,AQP6PL1000,ORACLE,,ORACLE,,AQL20050609.ID.AAA,,,Missing Login Information,1
136.61.212.129,PATASMMON,PATROLAG,136.61.212.179,136.61.212.130,IDP6PL1007-VIP.ID.AAA,#NAME?,JDBC THIN CLIENT,ORACLE,,AQP6PO06,,,Session Error,1
136.61.212.129,SYS,ORACLE,136.61.212.129,136.61.212.129,AQP6PO06,ORACLEPIDWPCD11,NBORAUTIL,ORACLE,,AQP6PO06,,,Session Error,1
136.60.214.34,PATASMMON,PATROLAG,136.61.212.179,136.61.212.130,ADP6PL1007-VIP.ID.AAA,#NAME?,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,1
136.61.213.95,PATASMMON,PATROLAG,136.61.213.95,136.61.212.62,AQP6PL1000,#NAME?,JDBC THIN CLIENT,ORACLE,,AQP6PL1000,,,Session Error,1
136.61.212.178,ASMSNMP,ORACLE,136.61.212.178,136.61.212.129,AQP6PO06,0,,ORACLE,,AQP6PO06,,,Session Error,1
10.87.22.22,?,,136.61.213.95,136.61.212.62,AQP6PL1000,ORACLE,,ORACLE,,AQL20050609.ID.AAA,,,Session Error,1
136.60.214.34,PATASMMON,PATROLAG,136.61.212.178,136.61.212.129,AQP6PO06-VIP.ID.AAA,#NAME?,JDBC THIN CLIENT,ORACLE,,AQP3NL1087,,,Session Error,1
'''
        return csv_content
    elif csvType == "trusted connection sessions":
        csv_content = '''Date,Client IP/Src App/DB User/Server IP/Svc. Name/OS User/DB Name,Count of Session Id
9-Oct,10.13.26.116+JDBC THIN CLIENT+PATASMMON+10.13.26.118++ASM+AATROCCC+,288
9-Oct,10.13.45.103+JDBC THIN CLIENT+PATASMMON+10.13.45.103++ASM+AATROCCC+,574
9-Oct,10.13.54.100+JDBC THIN CLIENT+PATASMMON+10.162.91.86++ASM+AATROCCC+,288
9-Oct,10.13.54.20+JDBC THIN CLIENT+PATASMMON+10.13.54.22++ASM+AATROCCC+,289
9-Oct,10.13.54.23+JDBC THIN CLIENT+PATASMMON+10.13.54.24++ASM+AATROCCC+,287
8-Oct,10.15.19.205+JDBC THIN CLIENT+PATASMMON+10.15.19.30++ASM+AATROCCC+,288
8-Oct,10.15.22.254+ORACLE+SYS+10.15.22.254++ASM2+ORACLE+,868
8-Oct,10.15.22.254+ORACLE+SYS+10.15.22.254++ASM2+AATROCCC+,576
8-Oct,10.15.22.254+ORAROOTAGENT.BIN+SYS+10.15.22.254++ASM2+ROOT+,288
8-Oct,10.15.22.254+SQLPLUS+SYS+10.15.22.254+ORACLE+ASM2+ORACLE+,253
8-Oct,10.15.25.58+JDBC THIN CLIENT+PATASMMON+10.15.25.60++ASM+AATROCCC+,286
7-Oct,10.15.25.76+JDBC THIN CLIENT+PATASMMON+10.15.25.76++ASM+AATROCCC+,515
7-Oct,10.15.25.76+JDBC THIN CLIENT+PATASMMON+10.15.25.77++ASM+AATROCCC+,256
7-Oct,10.15.25.76+JDBC THIN CLIENT+PATASMMON+10.164.241.88++ASM+AATROCCC+,506
6-Oct,10.15.25.76+JDBC THIN CLIENT+PATASMMON+10.164.241.89++ASM+AATROCCC+,258
6-Oct,10.162.153.51+JDBC THIN CLIENT+PATASMMON+10.15.25.60++ASM+AATROCCC+,285
5-Oct,10.162.63.32+JDBC THIN CLIENT+PATASMMON+10.13.45.103++ASM+AATROCCC+,120
5-Oct,10.162.91.85+JDBC THIN CLIENT+PATASMMON+10.162.91.86++ASM+AATROCCC+,289
5-Oct,10.164.155.49+JDBC THIN CLIENT+PATASMMON+10.13.26.118++ASM+AATROCCC+,145
5-Oct,10.164.171.55+JDBC THIN CLIENT+PATASMMON+10.13.54.22++ASM+AATROCCC+,288
5-Oct,10.164.171.59+JDBC THIN CLIENT+PATASMMON+10.13.54.24++ASM+AATROCCC+,287
5-Oct,10.164.240.120+JDBC THIN CLIENT+PATASMMON+10.15.22.254++ASM+AATROCCC+,288
5-Oct,10.164.240.120+JDBC THIN CLIENT+PATASMMON+10.164.240.122++ASM+AATROCCC+,578
4-Oct,10.164.240.120+JDBC THIN CLIENT+PATASMMON+10.164.240.123++ASM+AATROCCC+,288
4-Oct,10.164.240.122+ORACLE+SYS+10.164.240.122++ASM1+ORACLE+,1206
4-Oct,10.164.240.122+ORACLE+SYS+10.164.240.122++ASM1+AATROCCC+,1434
4-Oct,10.164.240.122+ORAROOTAGENT.BIN+SYS+10.164.240.122++ASM1+ROOT+,288
4-Oct,10.164.240.122+OSYSMOND.BIN+SYS+10.164.240.122++ASM1+ROOT+,280
4-Oct,10.164.240.122+SQLPLUS+SYS+10.164.240.122+ORACLE+ASM1+ORACLE+,253
3-Oct,10.164.240.123+ORACLE+SYS+10.164.240.123++ASM2+ORACLE+,482
3-Oct,10.164.240.123+ORACLE+SYS+10.164.240.123++ASM2+AATROCCC+,576
3-Oct,10.164.240.123+ORAROOTAGENT.BIN+SYS+10.164.240.123++ASM2+ROOT+,190
3-Oct,10.164.240.123+SQLPLUS+SYS+10.164.240.123+ORACLE+ASM2+ORACLE+,123
3-Oct,10.164.240.196+JDBC THIN CLIENT+PATASMMON+10.15.19.30++ASM+AATROCCC+,287
3-Oct,10.164.241.88+JDBC THIN CLIENT+PATASMMON+10.15.25.76++ASM+AATROCCC+,333
3-Oct,10.164.241.88+JDBC THIN CLIENT+PATASMMON+10.15.25.77++ASM+AATROCCC+,98
3-Oct,10.164.241.88+JDBC THIN CLIENT+PATASMMON+10.164.241.88++ASM+AATROCCC+,45
3-Oct,10.164.241.88+JDBC THIN CLIENT+PATASMMON+10.164.241.89++ASM+AATROCCC+,16
'''
        return csv_content
    elif csvType == "trusted connection sql":
        csv_content='''Date,Client IP/Src App/DB User/Server IP/Svc. Name/OS User/DB Name,Total access,Total access_1
9-Oct,10.164.240.199+FVAZZNT+ASMSNMP+10.164.240.992++ASM1+ORACLE+,3192,3192
9-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+MAIROLAH+,11520,11520
9-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+ORACLE+,3456,3456
9-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+MAIROLAH+,5760,5760
9-Oct,10.164.240.123+ORACLE+SYS+10.164.240.123++ASM2+MAIROLAH+,5760,5760
8-Oct,10.15.99.254+FVAZZNT+ASMSNMP+10.15.99.20++ASM2+ORACLE+,3192,3192
8-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+ORACLE+,3456,3456
8-Oct,10.15.25.63+FVAZZNT+ASMSNMP+10.15.25.114++ASM2+ORACLE+,2824,2824
8-Oct,10.164.93.56+FVAZZNT+ASMSNMP+10.164.93.81++ASM2+ORACLE+,2824,2824
7-Oct,10.164.240.199+FVAZZNT+ASMSNMP+10.164.240.992++ASM1+ORACLE+,3192,3192
7-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+MAIROLAH+,11480,11480
7-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+ORACLE+,3456,3456
7-Oct,10.15.99.254+FVAZZNT+ASMSNMP+10.15.99.20++ASM2+ORACLE+,3192,3192
6-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+MAIROLAH+,5740,5740
6-Oct,10.164.240.123+ORACLE+SYS+10.164.240.123++ASM2+MAIROLAH+,5740,5740
6-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+ORACLE+,3456,3456
6-Oct,10.13.101.60+JDBC THIN CLIENT+PMEGSP_APPUSER+10.162.91.130+VGT_LIVE.SASTIMS.AU.ABAB+VCAP+PAUDEGG1.SASTIMS.AU.ABAB@LAJUYHG12,2273,2273
5-Oct,10.13.101.102+JDBC THIN CLIENT+PMEGSP_APPUSER+10.162.91.130+VGT_LIVE.SASTIMS.AU.ABAB+VCAP+PAUDEGG1.SASTIMS.AU.ABAB@LAJUYHG12,2093,2093
5-Oct,10.164.240.199+FVAZZNT+ASMSNMP+10.164.240.992++ASM1+ORACLE+,3192,3192
5-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+MAIROLAH+,11520,11520
5-Oct,10.164.240.199+ORACLE+SYS+10.164.240.199++ASM1+ORACLE+,3456,3456
4-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+MAIROLAH+,5760,5760
4-Oct,10.15.99.254+FVAZZNT+ASMSNMP+10.15.99.20++ASM2+ORACLE+,3192,3192
4-Oct,10.164.240.123+ORACLE+SYS+10.164.240.123++ASM2+MAIROLAH+,5760,5760
4-Oct,10.15.99.254+ORACLE+SYS+10.15.99.254++ASM2+ORACLE+,3438,3438
'''
        return csv_content
    else:
        log.info("you did not specify CSV content")
        return csv_content

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = os.getenv(
    "ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"
)
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
MAX_RETRIES = 3  # Maximum number of retries for JSON parsing errors
MAX_INPUT_LENGTH = 1000  # Maximum length of user input query
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB maximum file size
MAX_DATAFRAME_ROWS = 100000  # Maximum number of rows in the dataframe
MAX_DATAFRAME_COLS = 100  # Maximum number of columns in the dataframe
EXECUTION_TIMEOUT = 30  # Maximum execution time for generated code in seconds

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/asvs_chat/templates"))


class CSVChatInputModel(BaseModel):
    """Model to validate input data for CSV chat queries."""

    query: str = Field(
        ..., description="The query about the CSV data", max_length=MAX_INPUT_LENGTH
    )
    #csv_content: Optional[str] = Field(None, description="The CSV content as a string")
    #file_url: Optional[HttpUrl] = Field(None, description="URL to a CSV or XLSX file")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def extract_column_unique_values(df: pd.DataFrame) -> str:
    """Extract unique values for each column in the dataframe."""
    column_info = []
    for column in df.columns:
        unique_values = df[column].dropna().unique()
        if len(unique_values) > 10:
            unique_values = unique_values[:10]
        column_info.append(f"{column}: {', '.join(map(str, unique_values))}")
    return "\n".join(column_info)


async def load_dataframe(
    csv_content: Optional[str] = None,
    #file_url: Optional[str] = None,
    #file: Optional[UploadFile] = None,
) -> pd.DataFrame:
    """Load a dataframe from various input sources."""
    log.debug("Attempting to load dataframe")
    if csv_content:
        log.debug("Loading dataframe from CSV content")
        df = pd.read_csv(StringIO(csv_content))
    else:
        raise ValueError(
            "No valid input source provided. Please specify the CSV content."
        )

    if df.shape[0] > MAX_DATAFRAME_ROWS or df.shape[1] > MAX_DATAFRAME_COLS:
        raise ValueError(
            f"Dataframe exceeds maximum allowed size of {MAX_DATAFRAME_ROWS} rows and {MAX_DATAFRAME_COLS} columns"
        )

    return df


def lower_if_string(x):
    """Convert to lowercase if the input is a string."""
    return x.lower() if isinstance(x, str) else x


def sanitize_user_input(input_str: str) -> Optional[str]:
    """
    Sanitize user input to prevent potential security issues.

    Args:
        input_str (str): The input string to be sanitized.

    Returns:
        Optional[str]: The sanitized input string if it's safe, or None if it contains blocked words.
    """
    blocklist = [
        "ignore",
        "previous prompt",
        "override",
        "bypass",
        "hack",
        "exploit",
        "vulnerability",
        "malicious",
        "inject",
        "execute",
        "sql",
        "delete",
        "drop",
        "truncate",
        "alter",
        "update",
        "insert",
        "create",
        "select",
        "union",
        "join",
        "where",
        "from",
        "script",
        "function",
        "eval",
        "exec",
        "system",
        "os",
        "subprocess",
        "import",
    ]

    log.debug(f"Sanitizing input: {input_str}")

    # Check if any blocked word is in the input
    for word in blocklist:
        if word in input_str.lower():
            log.warning(f"Blocked word '{word}' found in input")
            return None

    # If no blocked words are found, return the sanitized input
    sanitized_input = re.sub(r"[^\w\s.,?!-]", "", input_str)
    sanitized_input = sanitized_input.strip()[:MAX_INPUT_LENGTH]
    log.debug(f"Sanitized input: {sanitized_input}")
    return sanitized_input


async def process_csv_chat(
    df: pd.DataFrame, query: str, is_retry: bool = False, error_message: str = ""
) -> str:
    """Process the CSV chat query using pandas and LLM."""
    log.debug("Processing CSV chat query")
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].map(lower_if_string)

    column_info = extract_column_unique_values(df)
    df_head = str(df.head(5).to_markdown())

    sanitized_query = sanitize_user_input(query)
    log.debug(f"Sanitized query: {sanitized_query}")

    if is_retry:
        prompt_template = template_env.get_template("csv_chat_retry_prompt.jinja")
        prompt = prompt_template.render(
            df_head=df_head,
            column_info=column_info,
            query=sanitized_query,
            error_message=error_message,
        )
    else:
        prompt_template = template_env.get_template("csv_chat_prompt.jinja")
        prompt = prompt_template.render(
            df_head=df_head, column_info=column_info, query=sanitized_query
        )

    log.debug(f"Generated prompt: {prompt}")

    client = ICAClient()
    with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
        response_future = executor.submit(
            client.prompt_flow, model_id_or_name=DEFAULT_MODEL, prompt=prompt
        )
        response = await asyncio.to_thread(lambda: response_future.result())

    log.debug(f"Received LLM response: {response}")
    return response


def sanitize_code(code: str) -> str:
    """Sanitize the code to prevent common issues and ensure safety."""
    code = code.replace("'", '"')
    blocklist = [
        "eval",
        "exec",
        "import",
        "open",
        "os",
        "sys",
        "subprocess",
        "shutil",
        "__import__",
        "globals",
        "locals",
        "getattr",
        "setattr",
        "delattr",
        "compile",
        "timeit",
        "input",
        "raw_input",
        "breakpoint",
        "base64",
        "pickle",
        "shelve",
        "socket",
        "requests",
        "urllib",
        "http",
        "ftp",
        "while",
        "for",
        "class",
        "def",
        "lambda",
        "yield",
        "return",
        "raise",
        "try",
        "except",
        "finally",
        "with",
        "assert",
        "del",
        "global",
        "nonlocal",
    ]
    for word in blocklist:
        if re.search(r"\b" + re.escape(word) + r"\b", code):
            raise ValueError(f"Unsafe operation detected: {word}")

    allow_list = (
        [
            "print",
            "len",
            "str",
            "int",
            "float",
            "bool",
            "list",
            "dict",
            "set",
            "tuple",
            "sum",
            "min",
            "max",
            "sorted",
            "any",
            "all",
            "zip",
            "map",
            "filter",
            "round",
            "abs",
            "pow",
            "range",
            "contains",
            "DataFrame",
        ]
        + dir(pd.DataFrame)
        + dir(pd.Series)
        + dir(np)
    )

    function_pattern = re.compile(r"\b(\w+)\s*\(")
    for match in function_pattern.finditer(code):
        func_name = match.group(1)
        if func_name not in allow_list:
            raise ValueError(f"Unauthorized function detected: {func_name}")

    return code


def fix_syntax_errors(code: str) -> str:
    """Attempt to fix common syntax errors in the generated code."""
    lines = code.strip().split("\n")
    if not any(line.strip().startswith("result =") for line in lines):
        if len(lines) > 1:
            lines.append(f"result = {lines[-1]}")
        else:
            lines.append(f"result = {lines[0]}")
    return "\n".join(lines)


async def execute_code_with_timeout(exec_func: str, df: pd.DataFrame) -> str:
    """Execute the code with a timeout."""

    async def run_code():
        # Properly indent the user code
        indented_code = textwrap.indent(exec_func.strip(), "    ").replace("```python", "").replace("```", "")

        # Create the full function with proper indentation
        full_func = f"""
def exec_code(df):
    df = df.fillna('')
    result = None
{indented_code}
    return result
"""
        local_vars = {"df": df}
        exec(full_func, globals(), local_vars)
        return local_vars["exec_code"](df)

    try:
        result = await asyncio.wait_for(run_code(), timeout=EXECUTION_TIMEOUT)
        return result
    except asyncio.TimeoutError:
        raise ValueError(f"Code execution timed out after {EXECUTION_TIMEOUT} seconds")
    except IndentationError as ie:
        raise ValueError(f"Indentation error in generated code: {str(ie)}")
    except Exception as e:
        raise ValueError(f"Error executing generated code: {str(e)}")


async def chat_with_csv(
    query: str,
    csvType: str
    #query: str = Form(...),
    #csvType: str = Form(...),
    #csv_content: Optional[str] = Form(None),
    #file_url: Optional[str] = Form(None),
    #file: Optional[UploadFile] = File(None),
) -> OutputModel:
    """
    Handle POST requests to chat with CSV data.
    """
    invocation_id = str(uuid4())
    log.info(f"Processing chat request with invocation ID: {invocation_id}")

    log.debug(f"Original query: {query}")

    # Immediately check for unsafe input
    sanitized_query = sanitize_user_input(query)
    log.debug(f"Sanitized query: {sanitized_query}")

    if sanitized_query is None:
        log.warning(f"Unsafe input detected for invocation ID {invocation_id}")
        return OutputModel(
            status="error",
            invocationId=invocation_id,
            response=[
                ResponseMessageModel(
                    message="Error: Potentially insecure user input. Request rejected."
                )
            ],
        )

    csvType = csvType.lower().replace("_", " ")
    # Validate if csvType is one of permitted values
    types_allowed = ["asvs", "failed logins", "trusted connection sessions", "trusted connection sql"]
    if csvType not in types_allowed:
        formatted_types = ", ".join(types_allowed)
        raise HTTPException(status_code=400, detail=f"Invalid csvType. Allowed values are: {formatted_types}.")
    else:
        # set csv_content based on type specified
        csv_content = load_csv_content(csvType)

    try:
        # Load and validate the dataframe
        df = await safe_load_dataframe(csv_content)
        #df = await safe_load_dataframe(csv_content, file_url, file)
        log.info(
            f"Dataframe loaded successfully for invocation ID {invocation_id}. Shape: {df.shape}"
        )
    except ValueError as ve:
        log.error(
            f"Error loading dataframe for invocation ID {invocation_id}: {str(ve)}"
        )
        return OutputModel(
            status="error",
            invocationId=invocation_id,
            response=[ResponseMessageModel(message=f"Error: {str(ve)}")],
        )

    # Process the query with retries
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            log.debug(f"Processing query: {sanitized_query}")
            llm_response = await process_csv_chat(
                df,
                sanitized_query,
                is_retry=(retry_count > 0),
                error_message=f"Retry attempt {retry_count + 1}",
            )
            #print(f"original llm_response:\n{llm_response}") # for debugging
            llm_response = llm_response.replace("```json", "").replace("```python", "").replace("```", "").strip()
            #print(f"llm_response:\n{llm_response}") # for debugging
            log.info(f"LLM Response received for invocation ID: {invocation_id}")
            parsed_response = json.loads(llm_response)
            #print(f"parsed_response:\n{parsed_response}") # for debugging
            break
        except json.JSONDecodeError as json_error:
            log.warning(
                f"Failed to parse LLM response as JSON for invocation ID {invocation_id}. Attempt {retry_count + 1}. Error: {str(json_error)}"
            )
            retry_count += 1
            if retry_count == MAX_RETRIES:
                log.error(
                    f"Max retries reached for invocation ID {invocation_id}. Unable to parse LLM response as JSON."
                )
                return OutputModel(
                    status="error",
                    invocationId=invocation_id,
                    response=[
                        ResponseMessageModel(
                            message="Unable to process the query due to an internal error."
                        )
                    ],
                )

    result = "Unable to process the query. The LLM did not provide executable code."

    if "code" in parsed_response and parsed_response["code"]:
        python_code = parsed_response["code"]
        log.debug(
            f"Original generated code for invocation ID {invocation_id}: {python_code}"
        )

        try:
            python_code = sanitize_code(python_code)
            python_code = fix_syntax_errors(python_code)
            log.debug(
                f"Sanitized and fixed code for invocation ID {invocation_id}: {python_code}"
            )
        except ValueError as ve:
            log.error(
                f"Code sanitization error for invocation ID {invocation_id}: {str(ve)}"
            )
            return OutputModel(
                status="error",
                invocationId=invocation_id,
                response=[
                    ResponseMessageModel(
                        message="Error: Unable to execute the generated code due to security concerns."
                    )
                ],
            )

        python_code = python_code.replace(
            ".str.contains(", ".str.lower().str.contains("
        )

        try:
            result = await execute_code_with_timeout(python_code, df)
        except ValueError as ve:
            log.error(
                f"Error executing code for invocation ID {invocation_id}: {str(ve)}"
            )
            result = f"Error executing code: {str(ve)}"

        log.debug(f"Execution result for invocation ID {invocation_id}: {result}")

        if isinstance(result, (pd.DataFrame, pd.Series)):
            result = result.to_string()
        elif isinstance(result, (list, np.ndarray)):
            result = ", ".join(map(str, result))
        else:
            result = str(result)

    response_template = template_env.get_template("csv_chat_response.jinja")
    rendered_response = response_template.render(
        query=sanitized_query, llm_response=parsed_response, result=result
    )

    log.info(f"Rendered response for invocation ID {invocation_id}")

    return OutputModel(
        status="success",
        invocationId=invocation_id,
        response=[ResponseMessageModel(message=rendered_response)],
    )


def add_custom_routes(app: FastAPI):
    @app.post("/experience/local_load_csv_chat/ask/invoke")
    async def invoke_chat_with_csv(
        query: str = Form(...),
        csvType: str = Form(...)
    ) -> OutputModel:
        # Call the standalone function inside the route
        return await chat_with_csv(query, csvType)

    @app.post("/system/local_load_csv_chat/info/invoke")
    async def get_csv_info(
        csvType: str = Form(...)
        #csv_content: Optional[str] = Form(None),
        #file_url: Optional[str] = Form(None),
        #file: Optional[UploadFile] = File(None),
    ) -> OutputModel:
        """Handle POST requests to get information about the CSV data."""
        invocation_id = str(uuid4())
        log.info(f"Processing CSV info request with invocation ID: {invocation_id}")

        try:
            #df = await load_dataframe(csv_content, file_url, file)
            df = await load_dataframe(csv_content)
            log.info(f"Dataframe loaded successfully. Shape: {df.shape}")

            info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "head": df.head().to_dict(orient="records"),
                "summary": df.describe().to_dict(),
            }

            # Add additional checks for data types and missing values
            info["missing_values"] = df.isnull().sum().to_dict()
            info["data_types"] = df.dtypes.astype(str).to_dict()

            log.debug(f"CSV info: {info}")
            response_message = ResponseMessageModel(message=json.dumps(info, indent=2))
            return OutputModel(invocationId=invocation_id, response=[response_message])

        except Exception as e:
            log.error(f"Error getting CSV info: {str(e)}")
            log.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Error getting CSV info: {str(e)}"
            )


def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate the dataframe against security constraints."""
    if df.shape[0] > MAX_DATAFRAME_ROWS:
        raise ValueError(
            f"Number of rows ({df.shape[0]}) exceeds the maximum allowed ({MAX_DATAFRAME_ROWS})"
        )
    if df.shape[1] > MAX_DATAFRAME_COLS:
        raise ValueError(
            f"Number of columns ({df.shape[1]}) exceeds the maximum allowed ({MAX_DATAFRAME_COLS})"
        )

    total_size = df.memory_usage(deep=True).sum()
    if total_size > MAX_FILE_SIZE:
        raise ValueError(
            f"Dataframe size ({total_size} bytes) exceeds the maximum allowed ({MAX_FILE_SIZE} bytes)"
        )


async def safe_load_dataframe(
    csv_content: Optional[str] = None,
    #file_url: Optional[str] = None,
    #file: Optional[UploadFile] = None,
) -> pd.DataFrame:
    """Safely load a dataframe from various input sources with additional security checks."""
    df = await load_dataframe(csv_content)
    #df = await load_dataframe(csv_content, file_url, file)
    validate_dataframe(df)
    return df
