# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import unittest

from airflow.gcp.hooks.speech_to_text import GCPSpeechToTextHook
from tests.compat import patch, PropertyMock
from tests.gcp.utils.base_gcp_mock import mock_base_gcp_hook_default_project_id

PROJECT_ID = "project-id"
CONFIG = {"ecryption": "LINEAR16"}
AUDIO = {"uri": "gs://bucket/object"}


class TestTextToSpeechOperator(unittest.TestCase):
    def setUp(self):
        with patch(
            "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook.__init__",
            new=mock_base_gcp_hook_default_project_id,
        ):
            self.gcp_speech_to_text_hook = GCPSpeechToTextHook(gcp_conn_id="test")

    @patch("airflow.gcp.hooks.speech_to_text.GCPSpeechToTextHook.client_info", new_callable=PropertyMock)
    @patch("airflow.gcp.hooks.speech_to_text.GCPSpeechToTextHook._get_credentials")
    @patch("airflow.gcp.hooks.speech_to_text.SpeechClient")
    def test_speech_client_creation(self, mock_client, mock_get_creds, mock_client_info):
        result = self.gcp_speech_to_text_hook.get_conn()
        mock_client.assert_called_once_with(
            credentials=mock_get_creds.return_value,
            client_info=mock_client_info.return_value
        )
        self.assertEqual(mock_client.return_value, result)
        self.assertEqual(self.gcp_speech_to_text_hook._client, result)

    @patch("airflow.gcp.hooks.speech_to_text.GCPSpeechToTextHook.get_conn")
    def test_synthesize_speech(self, get_conn):
        recognize_method = get_conn.return_value.recognize
        recognize_method.return_value = None
        self.gcp_speech_to_text_hook.recognize_speech(config=CONFIG, audio=AUDIO)
        recognize_method.assert_called_once_with(config=CONFIG, audio=AUDIO, retry=None, timeout=None)
