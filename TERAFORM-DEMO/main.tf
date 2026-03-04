# Terraform provider hasicrop/google v-7
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.21.0"
    }
  }
}


# providers GCP

provider "google" {
  project = "project-a48dc085-0e8c-4a6e-9ca"
  region  = "us-central1"
}

# Services - GCS

resource "google_storage_bucket" "demobucket00182734" {
  name          = "demobucket00182734"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }
}
