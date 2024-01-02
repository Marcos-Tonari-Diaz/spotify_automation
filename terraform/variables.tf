# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# Input variable definitions

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-2"
}

variable "spotify_client_id" {
  description = "Spotify App Client ID"

  type    = string
  default = "fa4954c77aad4069b8cb0833a79f5eb6"
}

variable "spotify_client_secret" {
  description = "Spotify App Client ID"

  type    = string
  default = "d9b4d63521834fe0bc3a184320a3609a"
}
